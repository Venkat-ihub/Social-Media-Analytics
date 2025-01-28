from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobPostForm
from .models import JobPost
from .facebook import facebook
from .instagram import instagram
from .linkedin import linkedin
import logging

# Set up logging
logger = logging.getLogger(__name__)

def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the job post
            job_post = form.save()
            # Redirect to the job posting page with buttons for each platform
            return redirect('post_job', job_post_id=job_post.id)
    else:
        form = JobPostForm()

    return render(request, 'my_app/create_job_post.html', {'form': form})

def post_job(request, job_post_id):
    job_post = get_object_or_404(JobPost, id=job_post_id)
    message = None  # To show success or error messages for specific platforms

    if request.method == 'POST':
        # Handle individual platform posting
        if 'post_to_facebook' in request.POST:
            try:
                # Ensure media exists before passing it
                media_path = job_post.media.path if job_post.media else None
                facebook(f"{job_post.title}: {job_post.description}", media_path)
                message = "Posted to Facebook successfully!"
            except Exception as e:
                message = f"Failed to post to Facebook: {e}"
                logger.error(f"Error posting to Facebook: {e}")

        elif 'post_to_instagram' in request.POST:
            try:
                instagram(job_post)
                message = "Posted to Instagram successfully!"
            except Exception as e:
                message = f"Failed to post to Instagram: {e}"
                logger.error(f"Error posting to Instagram: {e}")

        elif 'post_to_linkedin' in request.POST:
            try:
                linkedin(job_post)
                message = "Posted to LinkedIn successfully!"
            except Exception as e:
                message = f"Failed to post to LinkedIn: {e}"
                logger.error(f"Error posting to LinkedIn: {e}")

    return render(request, 'my_app/post_job.html', {'job_post': job_post, 'message': message})
