# main_pages/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm # <--- Make sure this line is present
from django.template import TemplateDoesNotExist
from django.http import FileResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re # Regular expressions for parsing
import PyPDF2 # Make sure PyPDF2 is imported if used in extract_text_from_pdf
from django.views.decorators.http import require_GET, require_POST
from django.contrib.gis.geoip2 import GeoIP2
from .models import ResumeDownload
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# --- Corrected API Key Configuration ---
API_KEY_NAME = "GOOGLE_API_KEY" # The name of the variable in your .env file
google_api_key = os.getenv(API_KEY_NAME)

print(f"Checking for environment variable: {API_KEY_NAME}") # Debugging
if google_api_key:
    print("API Key found, configuring genai...") # Debugging
    genai.configure(api_key=google_api_key)
else:
    # Critical Error: Log this or raise an exception in a real app
    print(f"ERROR: Environment variable '{API_KEY_NAME}' not found or is empty!")
    # Optionally, configure with a placeholder or handle the error gracefully
    # For now, we'll let the downstream error happen, but you should handle this
    pass
# --- End Correction ---

# Create your views here.
def home(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            try:
                messages.success(request, "Your message has been sent successfully! I'll get back to you soon.")
                return redirect('/#contact')
            except Exception as e:
                messages.error(request, "Sorry, there was an error sending your message. Please check server logs or try again later.")

        else:
            messages.error(request, "Please correct the errors below.")

    else: # GET request
        form = ContactForm() 

    context = {'form': form}
    return render(request, 'main_pages/home.html', context)

def project_detail_view(request, project_slug):
    template_name = f'main_pages/project_descriptions/{project_slug}.html'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        # Handle cases where the template doesn't exist (e.g., show a 404 page)
        return render(request, 'main_pages/project_not_found.html', status=404)  # Create this template

def project_not_found_view(request):
    return render(request, 'main_pages/project_not_found.html', status=404)


def travel_view(request):
    context = {}
    return render(request, 'main_pages/travel.html', context)

def artwork_view(request):
        return render(request, 'main_pages/artwork.html')
    
def tools_view(request):
        return render(request, 'main_pages/tools.html')

def tool_detail_view(request, tool_name):
    tool_names = {
        'resume_wizard': 'Resume Wizard',
        'job_match_pro': 'JobMatch Pro',
        'cover_craft': 'CoverCraft',
        'illustrate_ai': 'IllustrateAI',
        'code_explainer': 'Code Explainer',
        'skill_sprint': 'SkillSprint',
        'portfolio_pro': 'Portfolio Pro',
        'interview_ace': 'Interview Ace',  # Added this line
    }

    if tool_name in tool_names:
        context = {'tool_name': tool_names[tool_name]}
        return render(request, f'main_pages/tools/{tool_name}.html', context)
    else:
        return render(request, 'main_pages/tool_not_found.html', status=404)

def tool_not_found_view(request):
    return render(request, 'main_pages/tool_not_found.html', status=404)

def resume_wizard_view(request):
        return render(request, 'main_pages/tools/resume_wizard.html')

@csrf_exempt
def analyze_resume(request):
    print("analyze_resume view called")
    if not google_api_key: # Check if API key failed to load earlier
        print("Error: API Key not configured. Cannot analyze resume.")
        return JsonResponse({'score': 0, 'recommendations': ['Server configuration error: API Key missing.']}, status=500)

    if request.method == 'POST' and request.FILES.get('resume'): # Use .get() for safety
        resume_file = request.FILES['resume']
        print("Resume file received:", resume_file.name)
        file_path = default_storage.save('temp_resumes/' + resume_file.name, ContentFile(resume_file.read()))
        full_file_path = default_storage.path(file_path) # Get the full absolute path
        print(f"Resume saved temporarily to: {full_file_path}") # Debugging path

        resume_text = extract_text_from_pdf(full_file_path) # Pass the full path
        print("Extracted resume text:", resume_text[:200] + "..." if resume_text else "No text extracted.") # Print more text

        analysis = analyze_resume_with_gemini(resume_text)
        print("Analysis from LLM:", analysis)

        try:
            default_storage.delete(file_path)
            print(f"Temporary file deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting temporary file {file_path}: {e}")


        return JsonResponse({
            'score': analysis.get('score', 0), # Use .get() for safety
            'recommendations': analysis.get('recommendations', ['An unknown error occurred during analysis.'])
        })
    else:
        print("Invalid request to analyze_resume (Not POST or no 'resume' file)")
        return JsonResponse({'error': 'Invalid request. Must be POST with a "resume" file.'}, status=400)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from the uploaded PDF.
    Uses PyPDF2.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"PDF has {len(reader.pages)} pages.") # Debugging
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n" # Add newline between pages
                    else:
                        print(f"Warning: No text extracted from page {i+1}")
                except Exception as page_e:
                    print(f"Error extracting text from page {i+1}: {page_e}")
    except FileNotFoundError:
        print(f"Error: PDF file not found at path: {pdf_path}")
        return None # Indicate failure
    except Exception as e:
        print(f"Error opening or reading PDF file {pdf_path}: {e}")
        return None # Indicate failure
    return text

def analyze_resume_with_gemini(resume_text):
    """
    Analyze the resume text using the Gemini API.
    """
    if not resume_text:
        print("Error: Cannot analyze empty resume text.")
        return {'score': 0, 'recommendations': ["Error: Could not extract text from the resume PDF."]}

    # Check again if the key was configured (belt and suspenders)
    if not google_api_key:
        print("Error: Gemini API key not configured.")
        return {'score': 0, 'recommendations': ["Server configuration error: API Key missing."]}

    try:
        print("Attempting to call Gemini API...") # Debugging
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or your preferred model
        # More robust prompt:
        prompt = (
            "You are an expert resume reviewer. Analyze the following resume text. "
            "Provide a numerical score out of 10, where 10 is outstanding. "
            "Also, provide a list of specific, actionable recommendations for improvement. "
            "Format your response clearly, starting with 'Score: [score]/10' on one line, "
            "followed by 'Recommendations:' on the next line, and then each recommendation as a bullet point or numbered list item.\n\n"
            "Resume Text:\n"
            "------------\n"
            f"{resume_text}\n"
            "------------\n"
            "Analysis:"
        )
        response = model.generate_content(prompt)
        llm_response = response.text.strip()

        print("Raw LLM Response:", llm_response) # Debugging

        score, recommendations = parse_gemini_response(llm_response)
        return {'score': score, 'recommendations': recommendations}

    except Exception as e:
        print(f"Error analyzing resume with Gemini: {e}")
        # You might want to check the type of exception 'e' for more specific errors (e.g., AuthenticationError)
        return {'score': 0, 'recommendations': [f"Error communicating with the analysis service: {e}"]}

def parse_gemini_response(llm_response):
    """
    Parses the Gemini response to extract the score and recommendations.
    Assumes format:
    Score: [score]/10
    Recommendations:
    - Recommendation 1
    - Recommendation 2
    * Recommendation 3
    1. Recommendation 4
    """
    score = 0 # Default score
    recommendations = ["Could not parse the analysis response."] # Default recommendations

    try:
        # Extract score using regex
        score_match = re.search(r"Score:\s*(\d+)\s*/\s*10", llm_response, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))

        # Extract recommendations
        recommendations_section = re.split(r"Recommendations:", llm_response, maxsplit=1, flags=re.IGNORECASE)
        if len(recommendations_section) > 1:
            # Get text after "Recommendations:", strip whitespace, split into lines
            rec_lines = [line.strip() for line in recommendations_section[1].strip().split('\n')]
            # Filter out empty lines and list markers (-, *, digits.)
            recommendations = [re.sub(r"^\s*[-\*\d\.]+\s*", "", line) for line in rec_lines if line.strip() and re.sub(r"^\s*[-\*\d\.]+\s*", "", line)] # Ensure recommendation isn't empty after removing marker

        # Fallback if parsing failed but we got some text
        if not recommendations or (len(recommendations) == 1 and recommendations[0] == "Could not parse the analysis response."):
             if llm_response: # If there's *any* response text
                recommendations = [llm_response] # Just return the raw text as a single recommendation

    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        # Keep default score and recommendations in case of parsing error

    # Basic validation
    if not isinstance(score, int) or not (0 <= score <= 10):
        print(f"Warning: Parsed score '{score}' is invalid. Resetting to 0.")
        score = 0
    if not recommendations: # Ensure recommendations is never empty
        recommendations = ["No specific recommendations provided in the analysis."]


    print(f"Parsed Score: {score}") # Debugging
    print(f"Parsed Recommendations: {recommendations}") # Debugging
    return score, recommendations


def resume_jd_checker_view(request):
    """Renders the Resume-JD Checker tool page."""
    return render(request, 'main_pages/tools/job-match-pro.html')

# You can choose to use csrf_exempt or handle the CSRF token properly in your JS fetch request
@csrf_exempt # Make sure CSRF token is handled if you remove this (JS part updated to send header)
def analyze_match_view(request):
    """Handles the AJAX request for analyzing resume-JD match."""
    print("analyze_match_view called")
    if not google_api_key: # Check if API key was loaded (from previous setup)
        print("Error: API Key not configured.")
        return JsonResponse({'error': 'Server configuration error: API Key missing.'}, status=500)

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description', '').strip()

        if not resume_file:
            return JsonResponse({'error': 'Resume file is missing.'}, status=400)
        if not job_description:
            return JsonResponse({'error': 'Job description is missing.'}, status=400)

        print(f"Resume file received: {resume_file.name}")
        print(f"Job Description received (length): {len(job_description)}")

        file_path = default_storage.save('temp_resumes/' + resume_file.name, ContentFile(resume_file.read()))
        full_file_path = default_storage.path(file_path)
        print(f"Resume saved temporarily to: {full_file_path}")

        resume_text = extract_text_from_pdf(full_file_path) # Reuse your existing function

        # Clean up temp file immediately after text extraction
        try:
            default_storage.delete(file_path)
            print(f"Temporary file deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting temporary file {file_path}: {e}") # Log error but continue

        if resume_text is None:
            print("Error extracting text from PDF")
            return JsonResponse({'error': 'Could not extract text from the resume PDF.'}, status=500)
        if not resume_text.strip():
            print("Warning: Extracted resume text is empty.")
            # Decide if you want to proceed or return an error
            # return JsonResponse({'error': 'Extracted resume text is empty.'}, status=400)


        print("Extracted resume text (first 200 chars):", resume_text[:200] + "...")
        print("JD text (first 200 chars):", job_description[:200] + "...")

        # Call the specific analysis function for matching
        analysis_result = analyze_resume_jd_match(resume_text, job_description)
        print("Analysis result from LLM function:", analysis_result)

        return JsonResponse(analysis_result) # Return the structured result

    else:
        print("Invalid request method to analyze_match_view")
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)


def analyze_resume_jd_match(resume_text, jd_text):
    """
    Analyzes the match between resume text and job description using Gemini.
    """
    if not google_api_key: # Redundant check, but safe
        print("Error: Gemini API key not configured.")
        return {'score': None, 'analysis': ["Server configuration error: API Key missing."]}

    # More specific prompt for matching
    prompt = (
        "You are an expert hiring manager and resume analyzer. "
        "Compare the following Resume Text against the Job Description.\n"
        "1. Provide a concise Match Score as a percentage (e.g., 'Match Score: 85%'). Do not add any other text on this line.\n"
        "2. Provide a detailed Analysis and Recommendations section below the score. Start this section with 'Analysis and Recommendations:'.\n"
        "   - List key skills/keywords from the Job Description found in the resume.\n"
        "   - List important skills/keywords from the Job Description MISSING in the resume.\n"
        "   - Provide specific, actionable recommendations on how to tailor the resume *better* for THIS job description.\n"
        "   - Format the analysis points clearly, preferably as bullet points.\n\n"
        "Job Description:\n"
        "----------------\n"
        f"{jd_text}\n"
        "----------------\n\n"
        "Resume Text:\n"
        "------------\n"
        f"{resume_text}\n"
        "------------\n\n"
        "Analysis:"
    )

    try:
        print("Attempting to call Gemini API for resume-JD match...")
        # Ensure you have the model configured (should be done globally)
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or your preferred model
        response = model.generate_content(
            prompt,
            # Optional: Add safety settings if needed
            # safety_settings=[
            #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            #     # Add others as needed
            # ]
        )
        llm_response = response.text.strip()
        print("Raw LLM Response (Match):", llm_response) # Debugging

        score, analysis_points = parse_match_response(llm_response)
        return {'score': score, 'analysis': analysis_points}

    except Exception as e:
        print(f"Error analyzing resume-JD match with Gemini: {e}")
        # Provide more specific error info if possible (check Gemini error types)
        error_message = f"Error communicating with the analysis service: {e}"
        # Check for specific Gemini exceptions if the library provides them
        # Example: if isinstance(e, genai.types.StopCandidateException): error_message = ...
        return {'score': None, 'analysis': [error_message]}


def parse_match_response(llm_response):
    """
    Parses the Gemini response for the resume-JD match analysis.
    Expects:
    Match Score: [percentage]%
    Analysis and Recommendations:
    - Point 1
    - Point 2
    """
    score = None # Default score (percentage)
    analysis = ["Could not parse the analysis response."] # Default analysis

    try:
        # Extract score using regex (more robust)
        score_match = re.search(r"Match Score:\s*(\d{1,3})\s*%", llm_response, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))
            # Clamp score between 0 and 100 just in case
            score = max(0, min(100, score))


        # Extract analysis section (split by the header, case-insensitive)
        analysis_section = re.split(r"Analysis and Recommendations:", llm_response, maxsplit=1, flags=re.IGNORECASE)
        if len(analysis_section) > 1:
            # Get text after the header, strip whitespace, split into lines
            rec_lines = [line.strip() for line in analysis_section[1].strip().split('\n')]
            # Filter out empty lines and potentially list markers (-, *, digits.) for cleaner output
            analysis = [re.sub(r"^\s*[-\*\d\.]+\s*", "", line).strip() for line in rec_lines if line.strip()]
            # Ensure list isn't empty if filtering removed everything but there was text
            if not analysis and analysis_section[1].strip():
                analysis = [analysis_section[1].strip()] # Use raw text if filtering failed

        # Fallback if parsing failed but we got some text
        if not analysis or analysis[0] == "Could not parse the analysis response.":
             if llm_response: # If there's *any* response text
                # Try a simpler split if the primary parsing failed
                lines = [line.strip() for line in llm_response.split('\n') if line.strip()]
                if score is None and lines: # Try to find score on first line if regex failed
                    score_match_simple = re.search(r"(\d{1,3})\s*%", lines[0])
                    if score_match_simple:
                        score = int(score_match_simple.group(1))
                        score = max(0, min(100, score))
                        analysis = lines[1:] # Assume rest is analysis
                    else:
                        analysis = lines # Use all lines as analysis if score still not found
                elif lines:
                    analysis = lines # Use all lines if score was found but analysis parsing failed


    except Exception as e:
        print(f"Error parsing LLM match response: {e}")
        # Keep default score and analysis in case of parsing error, maybe add the error msg
        analysis = [f"Error parsing response: {e}"] + analysis

    # Basic validation / cleanup
    if score is None:
        print("Warning: Could not parse match score.")
    if not analysis: # Ensure analysis is never empty
        analysis = ["No specific analysis points could be extracted."]


    print(f"Parsed Match Score: {score}") # Debugging
    print(f"Parsed Analysis: {analysis}") # Debugging
    return score, analysis

def cover_letter_maker_view(request):
    """Renders the Cover Letter Crafter tool page."""
    # Assuming the template is saved as 'cover_craft.html' in the tools directory
    return render(request, 'main_pages/tools/cover_craft.html')

# Use @csrf_exempt or handle CSRF token in JS (JS updated to send header)
@csrf_exempt
def generate_cover_letter_view(request):
    """
    Handles the AJAX request for generating a cover letter.
    Now accepts either pasted resume text or an uploaded PDF file.
    """
    print("generate_cover_letter_view called")
    if not google_api_key: # Check if API key was loaded
        print("Error: API Key not configured.")
        return JsonResponse({'error': 'Server configuration error: API Key missing.'}, status=500)

    if request.method == 'POST':
        # Extract common data
        user_name = request.POST.get('user_name', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        job_title = request.POST.get('job_title', '').strip()
        hiring_manager_name = request.POST.get('hiring_manager_name', '').strip() # Optional
        job_description = request.POST.get('job_description', '').strip()
        skills_to_highlight = request.POST.get('skills_to_highlight', '').strip() # Optional
        resume_input_type = request.POST.get('resume_input_type', 'text') # 'text' or 'file'

        print(f"Resume input type received: {resume_input_type}")

        resume_text_for_llm = None
        temp_file_path = None # To track temporary file for deletion

        # --- Get Resume Info based on type ---
        if resume_input_type == 'file':
            resume_file = request.FILES.get('resume_file')
            if not resume_file:
                return JsonResponse({'error': 'Resume file is missing for upload type.'}, status=400)

            print(f"Processing uploaded resume file: {resume_file.name}")
            # Save temp file
            try:
                temp_file_path = default_storage.save('temp_resumes/' + resume_file.name, ContentFile(resume_file.read()))
                full_file_path = default_storage.path(temp_file_path)
                print(f"Resume saved temporarily to: {full_file_path}")
                # Extract text
                resume_text_for_llm = extract_text_from_pdf(full_file_path) # Use your existing function
                if resume_text_for_llm is None:
                    print("Error extracting text from PDF")
                    # Clean up temp file even if extraction failed
                    if temp_file_path:
                        default_storage.delete(temp_file_path)
                    return JsonResponse({'error': 'Could not extract text from the uploaded resume PDF.'}, status=500)
                if not resume_text_for_llm.strip():
                    print("Warning: Extracted resume text from PDF is empty.")
                    # Optional: return error or proceed with empty text
                    # return JsonResponse({'error': 'Extracted resume text from PDF is empty.'}, status=400)

            except Exception as e:
                print(f"Error processing uploaded file: {e}")
                # Clean up temp file if it exists on error
                if temp_file_path and default_storage.exists(temp_file_path):
                    default_storage.delete(temp_file_path)
                return JsonResponse({'error': f'Error handling uploaded file: {e}'}, status=500)
            finally:
                # Clean up temp file after text extraction (if path was set)
                if temp_file_path and default_storage.exists(temp_file_path):
                    try:
                        default_storage.delete(temp_file_path)
                        print(f"Temporary file deleted: {temp_file_path}")
                    except Exception as e:
                        print(f"Error deleting temporary file {temp_file_path}: {e}") # Log error but continue

        elif resume_input_type == 'text':
            resume_text_for_llm = request.POST.get('resume_text', '').strip()
            if not resume_text_for_llm:
                return JsonResponse({'error': 'Pasted resume text is missing.'}, status=400)
            print("Using pasted resume text.")
        else:
            return JsonResponse({'error': 'Invalid resume input type specified.'}, status=400)
        # --- End Get Resume Info ---


        # --- Basic Validation (Common Fields) ---
        if not all([user_name, company_name, job_title, job_description]):
            missing_fields = []
            if not user_name: missing_fields.append("Your Name")
            if not company_name: missing_fields.append("Company Name")
            if not job_title: missing_fields.append("Job Title")
            if not job_description: missing_fields.append("Job Description")
            # Resume text itself is validated above based on type
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"Validation Error: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        # ---

        # --- Proceed with Generation ---
        print("Data prepared for cover letter generation:")
        print(f"  User Name: {user_name}")
        print(f"  Company: {company_name}")
        print(f"  Job Title: {job_title}")
        print(f"  Hiring Manager: {hiring_manager_name or 'N/A'}")
        print(f"  Resume Len (for LLM): {len(resume_text_for_llm or '')}")
        print(f"  JD Len: {len(job_description)}")
        print(f"  Skills Highlight: {skills_to_highlight or 'N/A'}")


        # Call the specific generation function using the obtained resume text
        generation_result = generate_cover_letter_with_gemini(
            user_name=user_name,
            company_name=company_name,
            job_title=job_title,
            hiring_manager_name=hiring_manager_name,
            resume_text=resume_text_for_llm, # Use the processed text
            job_description=job_description,
            skills_to_highlight=skills_to_highlight
        )
        print("Result from LLM generation function:", generation_result)

        # Return JSON response (either cover_letter or error)
        return JsonResponse(generation_result)

    else:
        print("Invalid request method to generate_cover_letter_view")
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

def generate_cover_letter_with_gemini(**kwargs):
    """
    Generates a cover letter draft using the Gemini API based on provided details.

    Args:
        **kwargs: Dictionary containing user_name, company_name, job_title,
                hiring_manager_name, resume_text, job_description,
                skills_to_highlight.
    Returns:
        dict: {'cover_letter': generated_text} on success,
            {'error': error_message} on failure.
    """
    if not google_api_key:
        print("Error: Gemini API key not configured.")
        return {'error': "Server configuration error: API Key missing."}

    # --- Construct the Prompt ---
    prompt_parts = [
        f"You are a professional career advisor. Write a compelling and professional cover letter for {kwargs['user_name']} applying for the {kwargs['job_title']} position at {kwargs['company_name']}."
    ]
    if kwargs.get('hiring_manager_name'):
        prompt_parts.append(f"Address it to {kwargs['hiring_manager_name']} if possible (e.g., 'Dear {kwargs['hiring_manager_name']},'). If the name looks generic or incorrect, use a standard professional salutation like 'Dear Hiring Manager,' or 'Dear Hiring Team,'.")
    else:
        prompt_parts.append("Use a standard professional salutation like 'Dear Hiring Manager,' or 'Dear Hiring Team,'.")

    prompt_parts.extend([
        "\nThe cover letter should:",
        "- Express strong interest in the specific role and company.",
        "- Highlight relevant skills and experiences from the provided 'Resume Highlights' that match the 'Job Description'.",
        "- Directly reference key requirements mentioned in the 'Job Description' and explain how the candidate meets them.",
        "- Maintain a professional and enthusiastic tone.",
    ])

    if kwargs.get('skills_to_highlight'):
        prompt_parts.append(f"- Make sure to specifically emphasize the following points: {kwargs['skills_to_highlight']}.")

    prompt_parts.extend([
        "- Conclude with a call to action, expressing eagerness to discuss qualifications further.",
        "- Ensure standard cover letter formatting (address blocks are usually not needed in the text body itself, focus on paragraphs).",
        "\n--- Job Description ---\n",
        kwargs['job_description'],
        "\n--- Resume Highlights ---\n",
        kwargs['resume_text'],
        "\n--- Cover Letter Draft ---",
        "Please provide ONLY the text of the cover letter, starting with the salutation and ending with the closing and name. Do not include any extra commentary, headings, or explanations before or after the letter itself."
    ])
    full_prompt = "\n".join(prompt_parts)
    # --- End Prompt Construction ---

    # print("\nFull Prompt being sent to Gemini:\n", full_prompt[:500] + "...") # Debugging: Print start of prompt

    try:
        print("Attempting to call Gemini API for cover letter generation...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or your preferred model
        response = model.generate_content(
            full_prompt,
            # Optional: Add safety settings if needed
            # safety_settings=[ ... ]
        )

        # Accessing the generated text safely
        generated_text = ""
        if response.parts:
            generated_text = response.text # Use response.text for simplicity if available
        else:
            # Handle cases where the response might be blocked or empty
            print("Warning: Gemini response might be empty or blocked.")
            # You might want to check response.prompt_feedback for block reasons
            block_reason = response.prompt_feedback.block_reason if response.prompt_feedback else 'Unknown'
            return {'error': f"Failed to generate content. Reason: {block_reason}"}


        print("Raw LLM Response (Cover Letter):", generated_text[:300] + "...") # Debugging: Print start of response

        # Basic cleanup (optional: remove potential leading/trailing explanations if prompt fails)
        # generated_text = re.sub(r"^Here's the cover letter draft:\n+", "", generated_text, flags=re.IGNORECASE).strip()

        return {'cover_letter': generated_text.strip()}

    except Exception as e:
        print(f"Error generating cover letter with Gemini: {e}")
        # Consider logging the full exception details
        # import traceback
        # print(traceback.format_exc())
        return {'error': f"An error occurred while communicating with the generation service: {e}"}

# Assume your resume PDF is in your STATIC_ROOT or MEDIA_ROOT
# Or define a specific path in settings.py: RESUME_FILE_PATH = os.path.join(BASE_DIR, 'path', 'to', 'your_resume.pdf')
try:
    RESUME_FILENAME = "your_resume.pdf" # The actual filename
    # Construct path relative to BASE_DIR or use an absolute path from settings
    RESUME_FILE_PATH = os.path.join(settings.BASE_DIR, 'static', RESUME_FILENAME) # Example path
    if not os.path.exists(RESUME_FILE_PATH):
        # Fallback or alternative path if needed
        RESUME_FILE_PATH = os.path.join(settings.MEDIA_ROOT, RESUME_FILENAME) # Example media path
        if not os.path.exists(RESUME_FILE_PATH):
            logger.error(f"Resume file not found at configured paths.")
            RESUME_FILE_PATH = None # Ensure it's None if not found
except AttributeError:
    logger.error("RESUME_FILE_PATH not configured in settings or file missing.")
    RESUME_FILE_PATH = None


def get_client_ip(request):
    """Gets the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# This view *only* logs the download and confirms success.
# The actual download is triggered by the JavaScript separately AFTER this view confirms.
@require_POST # Use POST to indicate an action (logging the download)
def log_resume_download(request):
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    country, city, timezone = None, None, None
    try:
        geoip = GeoIP2()
        if ip_address:
            try:
                location_info = geoip.city(ip_address)
                country = location_info.get('country_name')
                city = location_info.get('city')
                timezone = location_info.get('time_zone')
            except Exception as e:
                logger.warning(f"Could not get GeoIP info for {ip_address} during download log: {e}")
    except Exception as e:
        logger.error(f"Could not initialize GeoIP2 for download log: {e}")


    try:
        ResumeDownload.objects.create(
            ip_address=ip_address,
            user_agent=user_agent,
            country=country,
            city=city,
            timezone=timezone
        )
        logger.info(f"Resume download logged for IP: {ip_address}")
        # Return the actual path to the resume file for the JS to use
        # Ensure the URL path is correctly configured in your urls.py to serve this file
        # Usually static files are served directly by the webserver (Nginx) in production
        # For simplicity here, we assume Django might serve it or provide the URL
        resume_url = os.path.join(settings.STATIC_URL, RESUME_FILENAME) # Example static URL
        # Or if using media: resume_url = os.path.join(settings.MEDIA_URL, RESUME_FILENAME)

        return JsonResponse({'status': 'success', 'resume_url': resume_url})
    except Exception as e:
        logger.error(f"Failed to log resume download for {ip_address}: {e}")
        return JsonResponse({'status': 'error', 'message': 'Could not log download.'}, status=500)


# Optional: A separate view to actually serve the file if not handled by Nginx/Whitenoise
@require_GET
def serve_resume_file(request):
    if RESUME_FILE_PATH and os.path.exists(RESUME_FILE_PATH):
        try:
            # Use FileResponse to efficiently serve the file
            # as_attachment=True forces the browser to download instead of display inline
            response = FileResponse(open(RESUME_FILE_PATH, 'rb'), as_attachment=True, filename=RESUME_FILENAME)
            return response
        except Exception as e:
            logger.error(f"Error serving resume file: {e}")
            return HttpResponseBadRequest("Error serving file.")
    else:
        logger.error("Attempted to serve resume file, but path is invalid or file missing.")
        return HttpResponseBadRequest("File not found.")