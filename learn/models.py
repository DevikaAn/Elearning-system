from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Registration(models.Model):
    Password = models.CharField(max_length=200, null=True)
    Registration_date = models.DateField(auto_now_add=True, null=True)
    Num_of_courses_enrolled = models.IntegerField(null=True)
    Num_of_courses_completed = models.IntegerField(null=True)
    Qualification = models.TextField(null=True)
    Introduction_brief = models.TextField(null=True)
    Image = models.ImageField(upload_to='media', null=True)
    Num_of_enrolled_students = models.IntegerField(null=True)
    Average_review_rating = models.IntegerField(null=True)
    Num_of_reviews = models.IntegerField(null=True)
    About_website = models.TextField(null=True)
    Registration_fee = models.IntegerField(null=True)
    User_role = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User,on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.First_name


class Category(models.Model):
    Category_title = models.CharField(max_length=200, null=True)
    Image = models.ImageField(null=True)

    def __str__(self):
        return self.Category_title


class Course(models.Model):
    Course_title = models.CharField(max_length=200, null=True)
    Course_brief = models.TextField(null=True)
    Course_duration = models.IntegerField(null=True)
    Course_fee = models.FloatField(null=True)
    Language = models.CharField(max_length=200, null=True)
    cou_cat = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,related_name = 'Course_to_category')
    cou_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name = 'Course_to_registration')

    def __str__(self):
        return self.Course_title


class Chapter(models.Model):
    Chapter_title = models.CharField(max_length=200, null=True)
    cha_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.Chapter_title


class Content(models.Model):
    Chapter_Content = models.FileField(upload_to='media', null = True)
    Chapter_text_content = models.TextField(max_length = 900, null=True)
    Chapter_Content_type = models.CharField(max_length=200, null=True)
    cont_cha = models.ForeignKey(Chapter, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.Chapter_Content_type


class Enrollment(models.Model):
    Pending_days = models.IntegerField(null=True)
    Enrollment_date = models.DateField(auto_now_add=True, null=True)
    Teacher_response = models.CharField(max_length=200, null=True)
    Course_completion_status = models.CharField(max_length=200, null=True)
    Payment_status = models.CharField(max_length=200, null=True)
    Certificate = models.FileField(null=True)
    notify = models.CharField(max_length=200, null = True)
    enrol_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True, related_name = 'student_enrolled')
    enrol_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='teacher_teaching')
    enrol_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='course_enrolled')


class Learning_progress(models.Model):
    Begin_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    Completion_timestamp = models.DateTimeField(auto_now=True, null=True)
    Status = models.CharField(max_length=200, null=True)
    Learn_p_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True, related_name='learning_progress_to_st_reg')
    Learn_p_tea_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True,related_name='learning_progress_to_tea_reg')
    Learn_p_cnt = models.ForeignKey(Content, on_delete=models.CASCADE, null=True,related_name='learning_progress_to_content')


class Feedback(models.Model):
    Rating_score = models.IntegerField(null=True)
    Feedback_text = models.TextField(null=True)
    Submission_date = models.DateField(auto_now_add=True,null=True)
    Feed_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True,related_name='feedback_st_reg')
    Feed_tea_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='feedback_tea_reg')
    Feed_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='feedback_to_course')


class Messages(models.Model):
    Message_content = models.TextField(null=True)
    From_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='from_message')
    To_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='to_message')


class Guest_messages(models.Model):
    Name = models.CharField(max_length = 200, null=True)
    Email = models.CharField(max_length=200, null=True)
    Message_content = models.TextField(null=True)


class Exam(models.Model):
    Question = models.TextField(null=True)
    Option1 = models.TextField(null=True)
    Option2 = models.TextField(null=True)
    Option3 = models.TextField(null=True)
    Correct_answer = models.TextField(null=True)
    Lock = models.CharField(max_length=200, null=True)
    Time_start = models.DateTimeField(null=True)
    Time_stop = models.DateTimeField(null=True)
    Exam_reg_st = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True, related_name = 'exam_to_student')
    Exam_reg_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name = 'exam_to_teacher')
    Exam_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='exam_to_course')


class Exam_results(models.Model):
    Total_marks = models.IntegerField(null=True)
    Acquired_marks = models.IntegerField(null=True)
    Grade = models.CharField(max_length=200, null = True)
    Time_stop = models.DateTimeField(auto_now=True, null = True)
    Exam_res_reg_st = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True, related_name = 'exam_res_to_student')
    Exam_res_reg_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True,related_name='exam_res_to_teacher')
    Exam_res_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='exam_res_to_course')


class Blogs(models.Model):
    Name = models.CharField(max_length=200, null = True)
    Blog_content = models.TextField(null=True)
    Image = models.ImageField(null=True)
    Date_blog = models.DateField(auto_now_add=True, null=True)
    Approval_status = models.CharField(max_length=200, null = True)


class Requests(models.Model):
    Name = models.CharField(max_length=200, null = True)
    User_category = models.CharField(max_length=200, null = True)
    Old_password = models.CharField(max_length=200, null = True)
    New_password = models.CharField(max_length=200, null = True)
    Req_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Newsletter(models.Model):
    Email = models.CharField(max_length=200, null = True)


class Attendance(models.Model):
    Date_tim = models.DateTimeField(auto_now_add=True, null=True)
    Attendance_done_location = models.CharField(max_length = 200, null = True)
    atten_stud = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name = 'att_to_student')
    atten_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='att_to_teacher')
    atten_enroll = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, related_name='att_to_enroll')


class Live(models.Model):
    ldate = models.TimeField(null=True)
    link = models.CharField(max_length = 200, null = True)
    enrol = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, related_name='liv_to_enrol')
    liv_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='liv_to_tea_reg')


class Assignment(models.Model):
    assignment_topic = models.CharField(max_length=200, null=True)
    assignment_upload = models.FileField(null=True)
    total_marks = models.CharField(max_length=200, null=True)
    pass_percent = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    submission_date = models.DateField(null=True)
    teacher_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='assignment_tea_reg')
    assign_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,related_name='assignment_to_course')


class Assignment_result(models.Model):
    assignment_upload_ans = models.FileField(null=True)
    acquired_marks = models.CharField(max_length=200, null=True)
    acquired_pass_percent = models.CharField(max_length=200, null=True)
    asssi_res_assi = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True,related_name='assignment_result_assi')
    asssi_res_st = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True,related_name='assignment_result_student')


class Exam_register(models.Model):
    ex_reg_cou = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,related_name='exam_register_course')
    ex_reg_st = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True,related_name='exam_register_student')
    ex_reg_tea = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, related_name='exam_register_teacher')
    ex_reg_st_enroll = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True,related_name='exam_register_student_enrollment')


class Course_st_stop(models.Model):
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    cou_st_stop_cou = models.ForeignKey(Course, on_delete = models.CASCADE, null=True, related_name='Course_st_stop_to_course')