from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from .forms import StudentRegistrationForm,StudentProfileForm,CompanyForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils.timezone import now
# Create your views here.



def custom_logout(request):
    logout(request)
    return redirect('guest_home') 


def register(request):
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request,user)
            return redirect('guest_home')
    else:
        user_form = StudentRegistrationForm()
        profile_form = StudentProfileForm()
    return render(request, 'register.html', {
    'user_form': user_form,
    'profile_form': profile_form
    })

def Home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')

        student = Student.objects.filter(user=request.user).first()
        companies = Company.objects.filter(deadline__gte=now())
        applications = application.objects.filter(student=student)

        return render(request, 'guest_home.html', {
            'is_student': True,
            'companies': companies,
            'applications': applications
        })

    return render(request, 'guest_home.html', {
        'is_student': False
    })
    
@login_required
def dashboard(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('student_home')

    # filter eligible companies
    companies = Company.objects.all()
    print(student)
    print(companies)

    return render(request, 'dashboard.html', {
        'companies': companies,
    })

@login_required
def apply_company(request, company_id):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('home')

    company = Company.objects.get(id=company_id)

    # already applied
    if application.objects.filter(student=student, company=company).exists():
        return redirect('student_home')

    # fix branch logic
    allowed = [b.strip().upper() for b in company.allowed_branches.split(',')]
    student_branch = student.branch.strip().upper()
    allowed = [b.strip().upper() for b in company.allowed_branches.split(',')]
    student_branch = student.branch.strip().upper()

    print("------ DEBUG ------")
    print("Student Branch:", student.branch)
    print("Allowed Branches RAW:", company.allowed_branches)
    print("Allowed Parsed:", allowed)
    print("Branch Match:", student_branch in allowed)

    print("Student CGPA:", student.cgpa)
    print("Required CGPA:", company.eligibility_cgpa)
    print("CGPA Match:", float(student.cgpa) >= float(company.eligibility_cgpa))

    if float(student.cgpa) >= float(company.eligibility_cgpa) and student_branch in allowed:
        application.objects.create(
            student=student,
            company=company,
            status='Applied'
        )
        print("✅ Application saved")
        print("Student Branch:", student.branch)


    else:
        print("❌ Not eligible")
        messages.error(request, "You are not eligible for this company")
    
        print("Allowed Branches Raw:", company.allowed_branches)
        print("Allowed Parsed:", allowed)
        print("Branch Match:", student_branch in allowed)

        print("Student CGPA:", student.cgpa)
        print("Required CGPA:", company.eligibility_cgpa)
        print("CGPA Match:", float(student.cgpa) >= float(company.eligibility_cgpa))

    return redirect('student_home')

@login_required
def company_dashboard(request):
    companies = Company.objects.filter(created_by = request.user)
    applications = application.objects.filter(company__in = companies)

    return render(request,'manage_applications.html',{
        'applications':applications
    })
@login_required
def admin_home(request):
    if not request.user.is_superuser:
        return redirect('guest_home')

    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    total_applications = application.objects.count()
    total_selected = application.objects.filter(status='Selected').count()

    recent_students = Student.objects.order_by('-id')[:2]
    recent_applications = application.objects.select_related('student', 'company').order_by('-id')[:5]

    upcoming_drives = Company.objects.filter(
        drive_date__gte=now()
    ).order_by('drive_date')[:5]

    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_applications': total_applications,
        'total_selected': total_selected,
        'recent_students': recent_students,
        'recent_applications': recent_applications,
        'upcoming_drives': upcoming_drives,
    }

    return render(request, 'admin_home.html', context)

from django.utils.timezone import now

@login_required
def student_home(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('home')

    # ✅ Only show active companies
    companies = Company.objects.filter(deadline__gte=now())

    applications = application.objects.filter(student=student)

    total_applications = applications.count()
    total_selected = applications.filter(status='Selected').count()

    eligible_companies = []

    for company in companies:
        allowed = [b.strip().upper() for b in company.allowed_branches.split(',')]
        
        if (
            float(student.cgpa) >= float(company.eligibility_cgpa) and
            student.branch.strip().upper() in allowed
        ):
            eligible_companies.append(company)

    applied_company_ids = applications.values_list('company_id', flat=True)

    context = {
        'companies': companies,
        'applications': applications,
        'total_applications': total_applications,
        'total_selected': total_selected,
        'eligible_companies':eligible_companies,
        'applied_company_ids': applied_company_ids,
    }

    return render(request, 'student_home.html', context)

@login_required
def company_detail(request, company_id):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('home')

    company = Company.objects.get(id=company_id)

    # check if already applied
    already_applied = application.objects.filter(
        student=student,
        company=company
    ).exists()

    return render(request, 'company_detail.html', {
        'company': company,
        'already_applied': already_applied
    })

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def update_application(request, app_id):

    # 🔒 Only superuser allowed
    if not request.user.is_superuser:
        raise PermissionDenied   # returns 403 (best practice)

    app = application.objects.get(id=app_id)

    if request.method == "POST":
        status = request.POST.get('status')

        if status == "Selected":
            app.status = "Selected"
            app.interview_date = request.POST.get('interview_date')
            app.interview_time = request.POST.get('interview_time')
            app.interview_mode = request.POST.get('interview_mode')
            app.interview_link = request.POST.get('interview_link')

        elif status == "Rejected":
            app.status = "Rejected"

        app.save()

    return redirect('manage_applications')


@login_required
def manage_companies(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            return redirect('manage_company')
    else:
        form = CompanyForm()

    companies = Company.objects.all().order_by('-id')

    return render(request, 'manage_companies.html', {
        'form': form,
        'companies': companies
    })

@login_required
def delete_company(request, company_id):
    if request.user.is_superuser:
        Company.objects.filter(id=company_id).delete()
    return redirect('manage_company')
@login_required
def manage_students(request):
    if not request.user.is_superuser:
        return redirect('home')

    students = Student.objects.select_related('user').all()

    # 🔍 Search
    query = request.GET.get('q')
    if query:
        students = students.filter(user__username__icontains=query)

    # 🎯 Branch filter
    branch = request.GET.get('branch')
    if branch:
        students = students.filter(branch=branch)

    # 🎯 Placement filter
    status = request.GET.get('status')
    if status == "placed":
        students = students.filter(application__status__iexact='Selected').distinct()
    elif status == "unplaced":
        students = students.exclude(application__status__iexact='Selected')

    # ✅ Add placement flag
    for student in students:
        student.is_placed = application.objects.filter(
            student=student,
            status__iexact='Selected'
        ).exists()

    return render(request, 'manage_students.html', {
        'students': students
    })

@login_required
def manage_applications(request):
    if not request.user.is_superuser:
        return redirect('home')

    applications = application.objects.select_related('student', 'company').all()

    return render(request, 'manage_applications.html', {
        'applications': applications
    })

@login_required
def student_profile(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return redirect('home')

    return render(request, 'student_profile.html', {
        'student': student
    })

@login_required
def mock_list(request):
    tests = MockTest.objects.all()
    return render(request, 'mock_list.html', {'tests': tests})

@login_required
def take_mock(request, test_id):
    test = MockTest.objects.get(id=test_id)
    questions = Question.objects.filter(mock_test=test)

    return render(request, 'take_mock.html', {
        'test': test,
        'questions': questions
    })

@login_required
def submit_mock(request, test_id):
    student = Student.objects.get(user=request.user)
    questions = Question.objects.filter(mock_test_id=test_id)

    score = 0
    total = questions.count()

    for q in questions:
        selected = request.POST.get(str(q.id))

        if selected:
            StudentAnswer.objects.create(
                student=student,
                question=q,
                selected_answer=selected
            )

            if selected == q.correct_answer:
                score += 1

    percentage = (score / total) * 100 if total > 0 else 0

    return render(request, 'mock_result.html', {
        'score': score,
        'total': total,
        'percentage': percentage
    })