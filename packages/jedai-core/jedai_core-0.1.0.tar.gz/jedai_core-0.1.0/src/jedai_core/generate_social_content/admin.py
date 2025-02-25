from django.contrib import admin

from .models import Inference, LiveSettings


@admin.register(LiveSettings)
class LiveSettingsAdmin(admin.ModelAdmin):
    list_display = ("model",)
    search_fields = ("model",)


@admin.register(Inference)
class InferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "model_alias", "run_on")
    readonly_fields = (
        "id",
        "detailed_instructions",
        "response",
        "model_alias",
        "run_on",
        "runtime",
    )
    search_fields = ("model_alias", "run_on")
    list_filter = ("run_on",)
    ordering = ("-run_on",)  # Ordena pelo mais recente
