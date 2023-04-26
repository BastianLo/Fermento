from django.contrib import admin

from .models import Batch, QrCode, Execution, JournalEntry

# Register your models here.

admin.site.register(Batch)
admin.site.register(QrCode)
admin.site.register(Execution)
admin.site.register(JournalEntry)
