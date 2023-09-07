from django.urls import path
import learn.views

urlpatterns = [
    path('',learn.views.home,name = 'home'),
    path('home',learn.views.home,name = 'home'),
    path('reg_msg', learn.views.reg_msg, name='reg_msg'),
    path('contact', learn.views.contact, name='contact'),
    path('register_st',learn.views.register_st,name = 'register_st'),
    path('news',learn.views.news,name = 'news'),
    path('about', learn.views.about, name='about'),
    path('register_tr',learn.views.register_tr,name = 'register_tr'),
    path('adminn',learn.views.admin_rg,name = 'adminn'),
    path('login/',learn.views.login,name = 'login'),
    path('add_blog', learn.views.add_blog, name='add_blog'),
    path('blogs_admin', learn.views.blogs_admin, name='blogs_admin'),

    path('cou_com_tea/<id>', learn.views.cou_com_tea, name='cou_com_tea'),
    path('cou_n_com_tea/<id>', learn.views.cou_n_com_tea, name='cou_n_com_tea'),

    path('blog_approves/<id>', learn.views.blog_approves, name='blog_approves'),
    path('blog_rejects/<id>', learn.views.blog_rejects, name='blog_rejects'),
    path('blog_delete/<id>', learn.views.blog_delete, name='blog_delete'),
    path('view_blog', learn.views.view_blog, name='view_blog'),
    path('update_pr_tr/', learn.views.update_pr_tr, name='update_pr_tr'),
    path('upl_cer', learn.views.upl_cer, name='upl_cer'),
    path('block', learn.views.block, name='block'),
    path('blocks/<id>', learn.views.blocks, name='blocks'),
    path('allows/<id>', learn.views.allows, name='allows'),
    path('allows1/<id>', learn.views.allows1, name='allows1'),
    path('feedbak', learn.views.feedbak, name='feedbak'),
    path('delete_feedback/<id>', learn.views.delete_feedback, name='delete_feedback'),
    path('m_m', learn.views.m_m, name='m_m'),
    path('del_msg_admin/<id>', learn.views.del_msg_admin, name='del_msg_admin'),
    path('reply_msg_admin/<id>', learn.views.reply_msg_admin, name='reply_msg_admin'),
    path('sent_msg_admin', learn.views.sent_msg_admin, name='sent_msg_admin'),

    path('g_m', learn.views.g_m, name='g_m'),
    path('delete_g_msg/<id>', learn.views.delete_g_msg, name='delete_g_msg'),
    path('reply_g_msg/<id>', learn.views.reply_g_msg, name='reply_g_msg'),


    path('subject_ad', learn.views.subject_ad, name='subject_ad'),
    path('edit_subject1/<id>/<idd>/<idt>/<pkm>', learn.views.edit_subject1, name='edit_subject1'),
    path('chapter_ad', learn.views.chapter_ad, name='chapter_ad'),
    path('edit_chapter1/<id>/<idd>/<idt>/<idk>/<pkm>', learn.views.edit_chapter1, name='edit_chapter1'),
    path('delete_chapter1/<id>/<idd>/<idt>/<idk>', learn.views.delete_chapter1, name='delete_chapter1'),
    path('ch_co_ad', learn.views.ch_co_ad, name='ch_co_ad'),
    path('edit_content1/<id>', learn.views.edit_content1, name='edit_content1'),
    path('logout', learn.views.logout, name='logout'),
    path('st_pr', learn.views.st_pr, name='st_pr'),
    path('ch_p11', learn.views.ch_p11, name='ch_p11'),


    path('course_tr/', learn.views.course_tr, name='course_tr'),
    path('edit_course_tr/<id>', learn.views.edit_course_tr, name='edit_course_tr'),
    path('delete_course_tr/<id>', learn.views.delete_course_tr, name='delete_course_tr'),
    path('add_course_tr', learn.views.add_course_tr, name='add_course_tr'),

    path('cat_admin', learn.views.cat_admin, name='cat_admin'),
    path('edit_cat_admin/<id>', learn.views.edit_cat_admin, name='edit_cat_admin'),
    path('delete_cat_admin/<id>', learn.views.delete_cat_admin, name='delete_cat_admin'),
    path('add_cat_admin', learn.views.add_cat_admin, name='add_cat_admin'),


    path('chapter_tr/<id>', learn.views.chapter_tr, name='chapter_tr'),
    path('edit_chapter_tr/<id>', learn.views.edit_chapter_tr, name='edit_chapter_tr'),
    path('delete_chapter/<id>', learn.views.delete_chapter, name='delete_chapter'),
    path('add_chapter', learn.views.add_chapter, name='add_chapter'),


    path('ch_co_tr/<id>', learn.views.ch_co_tr, name='ch_co_tr'),
    path('edit_content/<id>', learn.views.edit_content, name='edit_content'),
    path('delete_content/<id>', learn.views.delete_content, name='delete_content'),
    path('add_ch_con', learn.views.add_ch_con, name='add_ch_con'),

    path('delete_content1/<id>', learn.views.delete_content1, name='delete_content1'),



    path('stu_buk_acc', learn.views.stu_buk_acc, name='stu_buk_acc'),
    path('stu_accept/<id>', learn.views.stu_accept, name='stu_accept'),
    path('stu_reject/<id>', learn.views.stu_reject, name='stu_reject'),
    path('delete_test', learn.views.delete_test, name='delete_test'),
    path('delete_test1/<id>', learn.views.delete_test1, name='delete_test1'),
    path('exam_result', learn.views.exam_result, name='exam_result'),
    path('delete_ex_re/<id>', learn.views.delete_ex_re, name='delete_ex_re'),
    path('m_m1', learn.views.m_m1, name='m_m1'),
    path('del_msg_teacher/<id>', learn.views.del_msg_teacher, name='del_msg_teacher'),
    path('reply_msg_teacher/<id>', learn.views.reply_msg_teacher, name='reply_msg_teacher'),
    path('sent_msg_teacher', learn.views.sent_msg_teacher, name='sent_msg_teacher'),
    path('atten', learn.views.atten, name='atten'),
    path('st_book_courses', learn.views.st_book_courses, name='st_book_courses'),
    path('acc_chapter/<id>', learn.views.acc_chapter, name='acc_chapter'),
    path('acc_chapter1', learn.views.acc_chapter1, name='acc_chapter1'),
    path('compp', learn.views.compp, name='compp'),

    path('stu_sub_selnew', learn.views.stu_sub_selnew, name='stu_sub_selnew'),
    path('stu_sub_selnew1', learn.views.stu_sub_selnew1, name='stu_sub_selnew1'),
    path('stu_buk_teacher/<id>', learn.views.stu_buk_teacher, name='stu_buk_teacher'),


    path('stu_buk_teacherr/<id>', learn.views.stu_buk_teacherr, name='stu_buk_teacherr'),
    path('pay_stud_cours/<id>', learn.views.pay_stud_cours, name='pay_stud_cours'),

    path('pay_student', learn.views.pay_student, name='pay_student'),
    path('do_cer', learn.views.do_cer, name='do_cer'),
    path('update_pr_st/', learn.views.update_pr_st, name='update_pr_st'),
    path('feedback', learn.views.feedback, name='feedback'),
    path('ch_p', learn.views.ch_p, name='ch_p'),
    path('ch_p_admin', learn.views.ch_p_admin, name='ch_p_admin'),
    path('ex_not', learn.views.ex_not, name='ex_not'),
    path('start_test', learn.views.start_test, name='start_test'),
    path('save_exam', learn.views.save_exam, name='save_exam'),
    path('exam_result1', learn.views.exam_result1, name='exam_result1'),
    path('m_m2', learn.views.m_m2, name='m_m2'),
    path('del_msg_student/<id>', learn.views.del_msg_student, name='del_msg_student'),
    path('reply_msg_student/<id>', learn.views.reply_msg_student, name='reply_msg_student'),
    path('sent_msg_student', learn.views.sent_msg_student, name='sent_msg_student'),
    path('adm_prof/', learn.views.adm_prof, name='adm_prof'),
    path('del_admin/<id>', learn.views.del_admin, name='del_admin'),
    path('abb', learn.views.abb, name='abb'),
    path('edit_admin/', learn.views.edit_admin, name='edit_admin'),
    path('admin_home', learn.views.admin_home, name='admin_home'),
    path('student_home', learn.views.student_home, name='student_home'),
    path('teacher_home', learn.views.teacher_home, name='teacher_home'),
    path('pass_req', learn.views.pass_req, name='pass_req'),
    path('pass_req1/<id>', learn.views.pass_req1, name='pass_req1'),
    path('del_cer', learn.views.del_cer, name='del_cer'),
    path('delete_cert/<id>', learn.views.delete_cert, name='delete_cert'),
    path('blocks1/<id>', learn.views.blocks1, name='blocks1'),
    path('delete_subject1/<id>/<idd>/<idt>', learn.views.delete_subject1, name='delete_subject1'),
    path('stu_delete/<id>', learn.views.stu_delete, name='stu_delete'),
    path('notiffy', learn.views.notiffy, name='notiffy'),
    path('lang', learn.views.translate_language, name='lang'),
    path('news_let', learn.views.news_let, name='news_let'),
    path('cou_comp_st_tea', learn.views.cou_comp_st_tea, name='cou_comp_st_tea'),
    path('pay_teacher', learn.views.pay_teacher, name='pay_teacher'),
    path('pay_teacher_razor', learn.views.pay_teacher_razor, name='pay_teacher_razor'),

    path('face_template1', learn.views.face_template1, name='face_template1'),
    path('face_template2', learn.views.face_template2, name='face_template2'),
    path('TakeImages', learn.views.TakeImages, name='TakeImages'),
    path('TrackImages', learn.views.TrackImages, name='TrackImages'),
    path('view_stud_attendance',learn.views.view_stud_attendance,name='view_stud_attendance'),

    path('live_class', learn.views.live_class, name='live_class'),
    path('edit_live/<id>', learn.views.edit_live, name='edit_live'),
    path('delete_live/<id>', learn.views.delete_live, name='delete_live'),
    path('add_live', learn.views.add_live, name='add_live'),

    path('view_live', learn.views.view_live, name='view_live'),
    path('view_cat', learn.views.view_cat, name='view_cat'),
    path('view_cou/<id>', learn.views.view_cou, name='view_cou'),
    path('reg_course/<id>', learn.views.reg_course, name='reg_course'),


    path('assignment', learn.views.assignment, name='assignment'),
    path('add_assignment', learn.views.add_assignment, name='add_assignment'),
    path('edit_assignment/<id>', learn.views.edit_assignment, name='edit_assignment'),
    path('delete_assignment/<id>', learn.views.delete_assignment, name='delete_assignment'),

    path('upload_assi_tea', learn.views.upload_assi_tea, name='upload_assi_tea'),
    path('delete_assignment_upload/<id>', learn.views.delete_assignment_upload, name='delete_assignment_upload'),
    path('add_mark_assi_tea/<id>', learn.views.add_mark_assi_tea, name='add_mark_assi_tea'),

    path('exam_reg_stu', learn.views.exam_reg_stu, name='exam_reg_stu'),
    path('exam_reg_stu1', learn.views.exam_reg_stu1, name='exam_reg_stu1'),
    path('exam_reg_stu2/<id>', learn.views.exam_reg_stu2, name='exam_reg_stu2'),

    path('assi_st', learn.views.assi_st, name='assi_st'),

    path('atten_tea', learn.views.atten_tea, name='atten_tea'),

    path('sched_test_t1', learn.views.sched_test_t1, name='sched_test_t1'),
    path('sched_ex_cat', learn.views.sched_ex_cat, name='sched_ex_cat'),
    path('sched_test', learn.views.sched_test, name='sched_test'),
    path('sched_test1', learn.views.sched_test1, name='sched_test1'),
    path('sched_test3', learn.views.sched_test3, name='sched_test3'),

    path('atten_admin', learn.views.atten_admin, name='atten_admin'),
    path('attendance_between_date_admin', learn.views.attendance_between_date_admin, name='attendance_between_date_admin'),
    path('delete_atten_admin/<id>', learn.views.delete_atten_admin, name='delete_atten_admin'),
    path('pay_admin', learn.views.pay_admin, name='pay_admin'),

    path('attendance_between_date_teacher', learn.views.attendance_between_date_teacher, name='attendance_between_date_teacher'),

    path('payment_between_date_admin', learn.views.payment_between_date_admin,name='payment_between_date_admin'),

    path('courses_admin', learn.views.courses_admin, name='courses_admin'),
    path('course_between_date_admin', learn.views.course_between_date_admin, name='course_between_date_admin'),
]


