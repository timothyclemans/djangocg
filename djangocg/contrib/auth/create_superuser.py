"""
Create a superuser from the command line. Deprecated; use manage.py
createsuperuser instead.
"""

if __name__ == "__main__":
    from djangocg.core.management import call_command
    call_command("createsuperuser")
