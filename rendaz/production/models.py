"Django models for the production app"

import gzip
import json
import zlib
from pathlib import Path

from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class DazFile(models.Model):
    """A Daz Studio scene file (or really any DSON file)"""

    name = models.CharField(_("name"), max_length=255)
    raw_path = models.CharField(_("path"), max_length=255)

    class Meta:
        verbose_name = _("dazfile")
        verbose_name_plural = _("dazfiles")

    def __init__(self, *args, **kwargs):
        self._dson = None
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.path.name}"

    @property
    def path(self):
        return Path(self.raw_path)

    @path.setter
    def set_path(self, newpath):
        # Force Path objects to strings
        self.raw_path = str(newpath)

    def read_dson(self):
        "Return the DSON data from the file as a Python dict"
        if self._dson:
            return self._dson
        # DSON files can be saved with optional gzip compression, but the extension
        # doesn't change. We'll just have to try opening it both ways and see which
        # works.
        try:
            fh = gzip.open(self.raw_path)
            self._dson = json.load(fh)
        except (gzip.BadGzipFile, EOFError, zlib.error):
            fh = open(self.raw_path, mode="rb")
            self._dson = json.load(fh)
        return self._dson


class DazPreset(models.Model):
    """DazPreset is a DazFile that needs to be applied to a selected
    object in a scene, rather than simply merged into the scene. However, some presets
    do apply to the scene as a whole (e.g. render presets). So the scene object is
    optional."""

    name = models.CharField(_("name"), max_length=255)
    scene_object = models.CharField(
        _("scene object"), max_length=255, blank=True, null=True
    )
    dazfile = models.ForeignKey(
        DazFile, verbose_name=_("daz preset file"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("dazpreset")
        verbose_name_plural = _("dazpresets")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dazpreset_detail", kwargs={"pk": self.pk})


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
            "Default is MEDIA_DIR/slug/"
        ),
    )

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})


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
    dazfiles = models.ManyToManyField(DazFile, verbose_name=_("daz files"), blank=True)
    dazpresets = models.ManyToManyField(
        DazPreset, verbose_name=_("daz presets"), blank=True
    )

    class Meta:
        verbose_name = _("character")
        verbose_name_plural = _("characters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("character_detail", kwargs={"pk": self.pk})


class Location(models.Model):

    name = models.CharField(_("name"), max_length=255)
    # Locations CAN be reused across projects, e.g. for sequels
    projects = models.ManyToManyField(Project, verbose_name=_("projects"))
    dazfiles = models.ManyToManyField(DazFile, verbose_name=_("daz files"), blank=True)
    dazpresets = models.ManyToManyField(
        DazPreset, verbose_name=_("daz presets"), blank=True
    )

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})


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
    camera = models.CharField(
        _("camera"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "If blank, will use whatever camera is selected in the loaded scene file"
        ),
    )
    # A Shot always comes from a single scene file, plus a set of presets which are all
    # applied.
    scene_file = models.ForeignKey(
        DazFile,
        verbose_name=_("scene file"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    presets = models.ManyToManyField(DazPreset, verbose_name=_("presets"), blank=True)

    class Meta:
        verbose_name = _("shot")
        verbose_name_plural = _("shots")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shot_detail", kwargs={"pk": self.pk})
