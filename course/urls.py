from django.urls import path
from .views import *
urlpatterns = [
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('addCategory/', AddCategory.as_view(), name='addCategory'),
    path('delete_category/<int:category_id>/', DeleteCategory.as_view(), name='delete_category'),
    path('upload_course/', UploadCourse.as_view(), name='upload_course'),
    path('upload_course_videos/<int:course_id>/', UploadCourseVideo.as_view(), name='upload_course_videos'),
    path('course_list/', CourseView.as_view(), name='course_list'),
    path('chef_course_list/<int:user_id>/', ChefCourseView.as_view(), name='course_list'),
    path('chef_course_Unlist/<int:user_id>/', ChefUnListCourseView.as_view(), name='chef_course_Unlist'),
    path('chef_course_listed/<int:user_id>/', ChefListedCourseView.as_view(), name='chef_course_listed'),

    path('chef/courses/<int:chefId>/', CourseListByChefs.as_view(), name='course-list-by-chefs'),
    path('courses/category/<int:category>/', CourseListByCategory.as_view(), name='course-list-by-category'),

    path('courses_videos/<int:course_id>/', CoursesVideosView.as_view(), name='courses_videos'),

    path('edit_course_video/<int:video_id>/', EditCourse.as_view(), name='edit_course_video'),
    path('delete_course_video/<int:video_id>/', DeleteCourseVideo.as_view(), name='delete_course_video'),
    path('delete_course/<int:course_id>/', DeleteCourse.as_view(), name='delete_course'),
    path('mark_course_as_listed/<int:course_id>/', MarkCourseListed.as_view(), name='mark_course_as_listed'),
    path('fetch_instructor/<int:instructor_id>/', InstructorsList.as_view(), name='fetch_instructor'),
    path('check_course_purchase_status/<int:courseId>/<str:user>/', CheckCoursePurchaseStatus.as_view(), name='check_course_purchase_status'),

    path('courses_user_purchased/<int:user_id>/', PurchasedCourses.as_view(), name='courses_user_purchased'),
    path('courses_videos_user_purchased/<int:course_id>/', PurchasedCoursesVideos.as_view(), name='courses_videos_user_purchased'),
    path('check_user_subscribed/<str:user_name>/', CheckUserPurchased.as_view(), name='check_user_subscribed'),
    path('chef_earnings/<int:user_id>/', ChefEarningsView.as_view(), name='chef_earnings'),


]