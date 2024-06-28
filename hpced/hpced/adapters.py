from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import GlobusToken

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        print("populate_user run")
        breakpoint()
        super().populate_user(request, sociallogin)
        extra_data = sociallogin.token.token
        user = sociallogin.user
        provider = sociallogin.account.provider
        resource_server = sociallogin.resource_server
        access_token = sociallogin.access_token
        refresh_token = sociallogin.secret_token
        expires_in = sociallogin.expires_in
        scope = sociallogin.scope
        GlobusToken.objects.update_or_create(
            user=user,
            provider=provider,
            resource_server=resource_server,
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': GlobusToken.calculate_expiration(expires_in),
                'scope': scope
            }        
        )

        # Check if the response contains other tokens
        if 'other_tokens' in extra_data:
            for token in extra_data['other_tokens']:
                resource_server = token['resource_server']
                access_token = token['access_token']
                refresh_token = token.get('refresh_token')
                expires_in = token['expires_in']
                scope = token['scope']

                # Save these tokens in your database or however you need to store them
                # Example: Assuming you have a model to store these tokens
                GlobusToken.objects.update_or_create(
                    user=user,
                    provider=provider,
                    resource_server=resource_server,
                    defaults={
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'expires_at': GlobusToken.calculate_expiration(expires_in),
                        'scope': scope
                    }
                )
