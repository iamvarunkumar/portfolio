from django.urls import path
from . import views # Import views from the current directory

app_name = 'main_pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/<slug:project_slug>/', views.project_detail_view, name='project_detail'),
    path('travel/', views.travel_view, name='travel'),
    path('project/not-found/', views.project_not_found_view, name='project_not_found'),
    path('artwork/', views.artwork_view, name='artwork'),
    path('tools/', views.tools_view, name='tools'),
    path('tools/resume-wizard/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'resume_wizard'}),
    path('tools/resume-wizard/analyze/', views.analyze_resume, name='analyze_resume'),  # This is crucial!
    path('tools/job-match-pro/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'job_match_pro'}),
    path('tools/job-match-pro/analyze/', views.analyze_match_view, name='analyze_resume_jd_match'), # Analysis endpoint for the new tool
    #path('tools/job-match-pro/', views.resume_jd_checker_view, name='job-match-pro'), # Page view for the new tool
    # Cover Letter Crafter (New) - Using 'cover_craft' in URL slug
    path('tools/cover-craft/', views.cover_letter_maker_view, name='cover_letter_maker'), # Page view for the tool
    path('tools/cover-craft/generate/', views.generate_cover_letter_view, name='generate_cover_letter'), # Generation endpoint

    path('tools/illustrate-ai/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'illustrate_ai'}),
    path('tools/code-explainer/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'code_explainer'}),
    path('tools/skill-sprint/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'skill_sprint'}),
    path('tools/portfolio-pro/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'portfolio_pro'}),
    path('tools/interview-ace/', views.tool_detail_view, name='tool_detail', kwargs={'tool_name': 'interview_ace'}), # Added this line
        
        

# The empty string '' means the base URL
]