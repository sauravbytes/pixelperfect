import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from subprocess import Popen, PIPE

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for this endpoint
class GitHubWebhookView(View):
    def post(self, request, *args, **kwargs):
        # Check for the GitHub webhook secret if you want to verify
        # Add your GitHub webhook secret here
        GITHUB_SECRET = 'pixelperfectbysauravchoudhary'

        # Optional: You can verify the secret if you have one
        if request.headers.get('X-Hub-Signature') != GITHUB_SECRET:
            return JsonResponse({'error': 'Invalid webhook signature'}, status=403)

        # Process the webhook payload
        payload = json.loads(request.body.decode('utf-8'))
        ref = payload.get('ref')
        branch = ref.split('/')[-1] if ref else ''

        # Only trigger deployment for the main branch
        if branch == 'main':
            self.deploy_project()

        return JsonResponse({'status': 'success'}, status=200)

    def deploy_project(self):
        # Your custom deployment logic here
        # For example, pulling the latest code and restarting the server:
        process = Popen(
            ['git', 'pull', 'origin', 'main'],  # Pull latest code
            cwd='/var/www/pixelperfect',  # The directory of your project
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = process.communicate()
        if err:
            print(f"Error: {err.decode()}")
        else:
            print(f"Output: {out.decode()}")
        # Optionally restart your server if required
        # Example: Restarting a service or server
        Popen(['pm2', 'restart', 'pixelperfect_gunicorn.service'])  # Use PM2 or any other service manager