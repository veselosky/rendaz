# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CategoryContent(models.Model):
    content = models.ForeignKey('Content', models.DO_NOTHING)
    category = models.ForeignKey('Tblcategories', models.DO_NOTHING)
    is_vendor = models.BooleanField()
    show_vendor_categorization = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'category_content'
        unique_together = (('content', 'category'),)


class CompatibilityBaseContent(models.Model):
    content = models.ForeignKey('Content', models.DO_NOTHING)
    compatibility_base = models.ForeignKey('Tblcompatibilitybase', models.DO_NOTHING)
    is_vendor = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'compatibility_base_content'
        unique_together = (('content', 'compatibility_base'),)


class Config(models.Model):
    conf_key = models.CharField(unique=True, max_length=64)
    conf_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'config'


class Content(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    product_path = models.CharField(max_length=4000, blank=True, null=True)
    filename = models.TextField()  # This field type is a guess.
    default_filename = models.TextField(blank=True, null=True)  # This field type is a guess.
    path = models.TextField()  # This field type is a guess.
    file_and_path = models.TextField()
    last_filesystem_path = models.TextField(blank=True, null=True)
    vendor_words = models.TextField()
    auto_words = models.TextField()
    user_words = models.TextField()
    description = models.ForeignKey('Tbldescription', models.DO_NOTHING, blank=True, null=True)
    note = models.ForeignKey('Tblnotes', models.DO_NOTHING, blank=True, null=True)
    content_type = models.ForeignKey('Tbltype', models.DO_NOTHING, blank=True, null=True)
    compatibility_base = models.ForeignKey('Tblcompatibilitybase', models.DO_NOTHING, blank=True, null=True)
    audience = models.SmallIntegerField(blank=True, null=True)
    group_num = models.IntegerField()
    hide = models.BooleanField()
    poser_type = models.SmallIntegerField(blank=True, null=True)
    studio_type = models.SmallIntegerField(blank=True, null=True)
    user_facing = models.BooleanField()
    hash = models.TextField()
    is_vendor = models.BooleanField()
    has_cloud_meta_data = models.BooleanField()
    is_installed = models.BooleanField()
    is_cloud_owned = models.BooleanField()
    needs_update = models.BooleanField()
    delete_on_update = models.BooleanField()
    date_created = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content'
        unique_together = (('product', 'path', 'filename'),)


class Customer(models.Model):
    remote_customer_id = models.IntegerField()
    store = models.ForeignKey('Tblstore', models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    key_test = models.CharField(max_length=255, blank=True, null=True)
    is_current = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'customer'
        unique_together = (('remote_customer_id', 'store'),)


class MigrationLink(models.Model):
    is_product = models.BooleanField(blank=True, null=True)
    old_id = models.BigIntegerField()
    new_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'migration_link'


class Product(models.Model):
    name = models.TextField()  # This field type is a guess.
    default_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    store = models.ForeignKey('Tblstore', models.DO_NOTHING, blank=True, null=True)
    token = models.TextField(blank=True, null=True)  # This field type is a guess.
    artists = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)
    guid = models.UUIDField(unique=True, blank=True, null=True)
    meta_hash = models.TextField(blank=True, null=True)
    file_hash = models.TextField(blank=True, null=True)
    thumbnail_hash = models.CharField(max_length=4000, blank=True, null=True)
    thumbnail_path = models.CharField(max_length=4000, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    date_purchased = models.DateTimeField(blank=True, null=True)
    group_num = models.IntegerField()
    hide = models.BooleanField()
    is_vendor = models.BooleanField()
    has_cloud_meta_data = models.BooleanField()
    is_installed = models.BooleanField()
    is_cloud_owned = models.BooleanField()
    needs_update = models.BooleanField()
    normalized_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    normalized_name_first_letter = models.CharField(max_length=1, blank=True, null=True)
    date_installed = models.DateTimeField(blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductOwner(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_owner'
        unique_together = (('product', 'customer'),)


class SerialNumber(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    serial_pool_id = models.IntegerField()
    serial_number = models.TextField()

    class Meta:
        managed = False
        db_table = 'serial_number'


class Sync(models.Model):
    customer = models.OneToOneField(Customer, models.DO_NOTHING, blank=True, null=True)
    master_meta_hash = models.TextField()
    master_file_hash = models.TextField()
    user_data_hash = models.TextField()
    last_sync_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sync'


class Tblbasepath(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldbasepath = models.TextField(db_column='fldBasePath')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblBasePath'


class Tblcategories(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.
    fldisunassigned = models.BooleanField(db_column='fldIsUnassigned')  # Field name made lowercase.
    fldnewcount = models.IntegerField(db_column='fldNewCount')  # Field name made lowercase.
    fldcategoryname = models.TextField(db_column='fldCategoryName')  # Field name made lowercase. This field type is a guess.
    fldcategoryparent = models.ForeignKey('self', models.DO_NOTHING, db_column='fldCategoryParent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblCategories'
        unique_together = (('fldcategoryparent', 'fldcategoryname'),)


class Tblcategoriescontent(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcontent = models.ForeignKey('Tblcontent', models.DO_NOTHING, db_column='fldContent', blank=True, null=True)  # Field name made lowercase.
    fldcategory = models.ForeignKey(Tblcategories, models.DO_NOTHING, db_column='fldCategory', blank=True, null=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblCategoriesContent'
        unique_together = (('fldcontent', 'fldcategory'),)


class Tblcompatibilitybase(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcompatibilitybase = models.TextField(db_column='fldCompatibilityBase')  # Field name made lowercase. This field type is a guess.
    fldisfilter = models.BooleanField(db_column='fldIsFilter')  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.
    fldcompatibilitybaseparent = models.ForeignKey('self', models.DO_NOTHING, db_column='fldCompatibilityBaseParent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblCompatibilityBase'
        unique_together = (('fldcompatibilitybaseparent', 'fldcompatibilitybase'),)


class Tblcontent(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldoriginalfilename = models.TextField(db_column='fldOriginalFilename')  # Field name made lowercase. This field type is a guess.
    fldoriginalpath = models.TextField(db_column='fldOriginalPath')  # Field name made lowercase. This field type is a guess.
    flddescriptionptr = models.ForeignKey('Tbldescription', models.DO_NOTHING, db_column='fldDescriptionPtr', blank=True, null=True)  # Field name made lowercase.
    fldnotesptr = models.ForeignKey('Tblnotes', models.DO_NOTHING, db_column='fldNotesPtr', blank=True, null=True)  # Field name made lowercase.
    fldcontenttype = models.ForeignKey('Tbltype', models.DO_NOTHING, db_column='fldContentType', blank=True, null=True)  # Field name made lowercase.
    fldcompatibilitybase = models.ForeignKey(Tblcompatibilitybase, models.DO_NOTHING, db_column='fldCompatibilityBase', blank=True, null=True)  # Field name made lowercase.
    fldnewcontent = models.BooleanField(db_column='fldNewContent')  # Field name made lowercase.
    fldaudience = models.SmallIntegerField(db_column='fldAudience')  # Field name made lowercase.
    fldhide = models.BooleanField(db_column='fldHide')  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.
    fldposertype = models.SmallIntegerField(db_column='fldPoserType')  # Field name made lowercase.
    fldstudiotype = models.SmallIntegerField(db_column='fldStudioType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblContent'
        unique_together = (('fldoriginalfilename', 'fldoriginalpath'),)


class Tblcontentcompatibilitybase(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcontent = models.ForeignKey(Tblcontent, models.DO_NOTHING, db_column='fldContent', blank=True, null=True)  # Field name made lowercase.
    fldcompatibilitybase = models.ForeignKey(Tblcompatibilitybase, models.DO_NOTHING, db_column='fldCompatibilityBase', blank=True, null=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblContentCompatibilityBase'
        unique_together = (('fldcontent', 'fldcompatibilitybase'),)


class Tblcontentfolders(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldbasepathid = models.ForeignKey(Tblbasepath, models.DO_NOTHING, db_column='fldBasePathID', blank=True, null=True)  # Field name made lowercase.
    fldnewcount = models.IntegerField(db_column='fldNewCount')  # Field name made lowercase.
    fldcontentfoldername = models.TextField(db_column='fldContentFolderName')  # Field name made lowercase. This field type is a guess.
    fldcontentfolderparent = models.ForeignKey('self', models.DO_NOTHING, db_column='fldContentFolderParent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblContentFolders'
        unique_together = (('fldcontentfolderparent', 'fldcontentfoldername', 'fldbasepathid'),)


class Tblcontentinstance(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldfilename = models.TextField(db_column='fldFilename')  # Field name made lowercase. This field type is a guess.
    fldcontent = models.ForeignKey(Tblcontent, models.DO_NOTHING, db_column='fldContent', blank=True, null=True)  # Field name made lowercase.
    fldpriority = models.BooleanField(db_column='fldPriority')  # Field name made lowercase.
    fldcontentfolder = models.ForeignKey(Tblcontentfolders, models.DO_NOTHING, db_column='fldContentFolder', blank=True, null=True)  # Field name made lowercase.
    fldnewcontent = models.BooleanField(db_column='fldNewContent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblContentInstance'
        unique_together = (('fldcontentfolder', 'fldfilename'),)


class Tblcontentkeyword(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcontent = models.ForeignKey(Tblcontent, models.DO_NOTHING, db_column='fldContent', blank=True, null=True)  # Field name made lowercase.
    fldassociation = models.ForeignKey('Tblkeyword', models.DO_NOTHING, db_column='fldAssociation', blank=True, null=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblContentKeyword'
        unique_together = (('fldcontent', 'fldassociation'),)


class Tbldescription(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    flddescription = models.TextField(db_column='fldDescription')  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblDescription'


class Tblkeyword(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldkeyword = models.TextField(db_column='fldKeyword', unique=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblKeyword'


class Tblnotes(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldnotes = models.TextField(db_column='fldNotes')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblNotes'


class Tblproduct(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldproductname = models.TextField(db_column='fldProductName')  # Field name made lowercase. This field type is a guess.
    fldsiteid = models.TextField(db_column='fldSiteID')  # Field name made lowercase. This field type is a guess.
    fldtoken = models.TextField(db_column='fldToken')  # Field name made lowercase. This field type is a guess.
    fldsupportfile = models.TextField(db_column='fldSupportFile')  # Field name made lowercase. This field type is a guess.
    fldartists = models.TextField(db_column='fldArtists')  # Field name made lowercase. This field type is a guess.
    flddescription = models.TextField(db_column='fldDescription')  # Field name made lowercase.
    fldguid = models.UUIDField(db_column='fldGuid', unique=True)  # Field name made lowercase.
    fldlastupdate = models.DateTimeField(db_column='fldLastUpdate')  # Field name made lowercase.
    fldhide = models.BooleanField(db_column='fldHide')  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.
    fldisminimeta = models.BooleanField(db_column='fldIsMiniMeta')  # Field name made lowercase.
    fldnormalizedname = models.TextField(db_column='fldNormalizedName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fldnormalizednamefirstletter = models.CharField(db_column='fldNormalizedNameFirstLetter', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProduct'


class Tblproductcontent(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcontent = models.ForeignKey(Tblcontent, models.DO_NOTHING, db_column='fldContent', blank=True, null=True)  # Field name made lowercase.
    fldproduct = models.ForeignKey(Tblproduct, models.DO_NOTHING, db_column='fldProduct', blank=True, null=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProductContent'
        unique_together = (('fldcontent', 'fldproduct'),)


class Tblrootcategories(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcategory = models.TextField(db_column='fldCategory')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblRootCategories'


class Tblsceneid(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldcompatibilitybase = models.ForeignKey(Tblcompatibilitybase, models.DO_NOTHING, db_column='fldCompatibilityBase', blank=True, null=True)  # Field name made lowercase.
    fldisvendor = models.BooleanField(db_column='fldIsVendor')  # Field name made lowercase.
    fldasseturi = models.TextField(db_column='fldAssetUri', unique=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblSceneID'


class Tblstore(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldsiteid = models.TextField(db_column='fldSiteID', unique=True)  # Field name made lowercase. This field type is a guess.
    fldtoken = models.TextField(db_column='fldToken')  # Field name made lowercase. This field type is a guess.
    fldurl = models.TextField(db_column='fldUrl')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblStore'


class Tbltype(models.Model):
    recid = models.BigAutoField(db_column='RecID', primary_key=True)  # Field name made lowercase.
    fldtype = models.TextField(db_column='fldType', unique=True)  # Field name made lowercase. This field type is a guess.
    flddefaultload = models.BooleanField(db_column='fldDefaultLoad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblType'


class UserData(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    user_key = models.CharField(max_length=255)
    user_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_data'
        unique_together = (('customer', 'user_key'),)
