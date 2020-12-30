"Django models for the production app"

import gzip
import json
import zlib
from pathlib import Path

from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Project(models.Model):

    name = models.CharField(_("working title"), max_length=255)
    title = models.CharField(_("release title"), max_length=255, blank=True)
    slug = models.SlugField(_("slug"), allow_unicode=True)
    artifacts_folder = models.CharField(
        _("artifacts folder"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "Where to store generated files for this project. "
            "Default is MEDIA_ROOT/slug/"
        ),
    )

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    @property
    def output_dir(self):
        if self.artifacts_folder:
            return Path(self.artifacts_folder)
        else:
            return Path(settings.MEDIA_ROOT) / self.slug


class Character(models.Model):

    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("Character's short name or speaking label"),
    )
    color = ColorField(
        _("accent color"),
        blank=True,
        null=True,
        help_text=_("Custom color for the dialog label (optional)"),
    )
    # Characters CAN be reused across projects, e.g. for sequels
    projects = models.ManyToManyField(Project, verbose_name=_("projects"))

    class Meta:
        verbose_name = _("character")
        verbose_name_plural = _("characters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("character_detail", kwargs={"pk": self.pk})


class Location(models.Model):

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    scene_file = models.CharField(
        _("scene file"), max_length=255, blank=True, null=True
    )
    # Locations CAN be reused across projects, e.g. for sequels
    projects = models.ManyToManyField(Project, verbose_name=_("projects"))

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})


class CharacterBuild(models.Model):
    """A Scene file with a representation of a Character.
    A Character is typically made up of a collection of assets: A figure,
    a hair asset, an outfit composed of several wearables, a makeup preset,
    possibly additional presets for hair and clothing. Since a character's
    hair, make-up, and clothing may change in different scenes through a story,
    you need multiple "builds" of the character for the different scenes. The
    DAZ file should be saved as a "scene subset".
    """

    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("Name of this build, e.g. 'Carrie - Dressed for Prom Night'"),
    )
    character = models.ForeignKey(
        Character, verbose_name=_("character"), on_delete=models.CASCADE
    )
    daz_file = models.CharField(_("DAZ file"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("character build")
        verbose_name_plural = _("character builds")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characterbuild_detail", kwargs={"pk": self.pk})


class Screenplay(models.Model):

    name = models.CharField(_("name"), max_length=255)
    # A Screenplay belongs to exactly one project (which can have multiple Screenplays,
    # e.g. per episode)
    project = models.ForeignKey(
        Project, verbose_name=_("project"), on_delete=models.CASCADE
    )
    # Upload directly for future analysis
    text_file = models.FileField(_("screenplay file"), upload_to=None, max_length=255)

    class Meta:
        verbose_name = _("screenplay")
        verbose_name_plural = _("screenplays")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("screenplay_detail", kwargs={"pk": self.pk})


class Shot(models.Model):

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    output_name = models.CharField(
        _("output name"),
        max_length=255,
        help_text=_("File name for the DAZ render settings output image"),
    )
    # A Shot always comes from a single scene file, plus a set of presets which are all
    # applied.
    scene_file = models.CharField(
        _("scene file"), max_length=255, blank=True, null=True
    )
    presets = models.JSONField(blank=True, null=True, help_text=_(""))
    camera = models.CharField(
        _("camera"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "If blank, will use whatever camera is selected in the loaded scene file"
        ),
    )

    class Meta:
        verbose_name = _("shot")
        verbose_name_plural = _("shots")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shot_detail", kwargs={"pk": self.pk})
