import os
import zipfile
import tempfile
import shutil
import plistlib
from django.db import models
from django.conf import settings
from sparkle.conf import SPARKLE_PRIVATE_KEY_PATH

class Application(models.Model):
    """A sparkle application"""
    
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    """A version for a given application"""
    
    application = models.ForeignKey(Application)
    
    title = models.CharField(max_length=100)
    version = models.CharField(blank=True, null=True, max_length=10)
    short_version = models.CharField(blank=True, null=True, max_length=50)
    dsa_signature = models.CharField(blank=True, null=True, max_length=80)
    length = models.CharField(blank=True, null=True, max_length=20)
    release_notes = models.TextField(blank=True, null=True)
    minimum_system_version = models.CharField(blank=True, null=True, max_length=10)
    published = models.DateTimeField(auto_now_add=True)
    update = models.FileField(upload_to='sparkle/')
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        super(Version, self).save(*args, **kwargs)
        
        update = False
        path = os.path.join(settings.MEDIA_ROOT, self.update.path)
        
        # if there is no dsa signature and a private key is provided in the settings
        if not self.dsa_signature and SPARKLE_PRIVATE_KEY_PATH and os.path.exists(SPARKLE_PRIVATE_KEY_PATH):
            command = 'openssl dgst -sha1 -binary < "%s" | openssl dgst -dss1 -sign "%s" | openssl enc -base64' % (path, SPARKLE_PRIVATE_KEY_PATH)
            process = os.popen(command)
            self.dsa_signature = process.readline().strip()
            process.close()
            update = True
        
        # if there is no length and it is a zip file
        # extract it to a tempdir and calculate the length
        # also parse the plist file for versions
        if not self.length and path.endswith('.zip'):
                zip_file = zipfile.ZipFile(path)
                tempdir = tempfile.mkdtemp()
                files = zip_file.namelist()
                start_path = None
                
                for f in files:
                    if f.endswith('/'):
                        d = os.path.join(tempdir, f)
                        if not start_path:
                            start_path = d        
                            os.makedirs(d)
                    else:
                        zip_file.extract(f, tempdir)
            
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(start_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                
                info_plist = os.path.join(start_path, 'Contents/Info.plist')

                if os.path.exists(info_plist):
                    plist = plistlib.readPlist(info_plist)
                    
                    if not self.version and 'CFBundleVersion' in plist:
                        self.version = plist.get('CFBundleVersion')
                    
                    if not self.short_version and 'CFBundleShortVersionString' in plist:
                        self.short_version = plist.get('CFBundleShortVersionString')     
                    
                    if not self.minimum_system_version and 'LSMinimumSystemVersion' in plist:
                        self.minimum_system_version = plist.get('LSMinimumSystemVersion')
                
                shutil.rmtree(tempdir)
                    
                self.length = total_size
                update = True
        
        if update:
            self.save()
            
        

class SystemProfileReport(models.Model):
    """A system profile report"""
    
    ip_address = models.IPAddressField()
    added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'SystemProfileReport'
    
class SystemProfileReportRecord(models.Model):
    """A key/value pair for a system profile report"""
    
    report = models.ForeignKey(SystemProfileReport)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=80)
    
    def __unicode__(self):
        return u'%s: %s' % (self.key, self.value)
