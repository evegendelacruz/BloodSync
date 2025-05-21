from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='approval_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]