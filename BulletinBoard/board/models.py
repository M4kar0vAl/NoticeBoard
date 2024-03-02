from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

class User(AbstractUser):
    subscriptions = ArrayField(models.CharField(max_length=2), size=10, default=list)


class Response(models.Model):
    text = models.TextField(verbose_name=_('Content'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Published at'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('Accepted'))
    advert = models.ForeignKey(to='Advert', on_delete=models.CASCADE, verbose_name=_('Advertisement'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('Author'))

    def accept(self):
        self.is_accepted = True
        self.save()

    def reject(self):
        self.delete()

    def __str__(self):
        return self.text


class Advert(models.Model):
    TANKS = 'TN'
    HEALERS = 'HL'
    DD = 'DD'
    MERCHANTS = 'ME'
    GUILDMASTERS = 'GM'
    QUESTGIVERS = 'QG'
    BLACKSMITHS = 'BS'
    LEATHERWORKERS = 'LW'
    POTIONMAKERS = 'PM'
    SPELLMASTERS = 'SM'
    CATEGORY_CHOICES = [
        ('', _('Choose Category')),
        (TANKS, _('Tanks')),
        (HEALERS, _('Healers')),
        (DD, _('Damage Dealers')),
        (MERCHANTS, _('Merchants')),
        (GUILDMASTERS, _('Guild Masters')),
        (QUESTGIVERS, _('Quest Givers')),
        (BLACKSMITHS, _('Blacksmiths')),
        (LEATHERWORKERS, _('Tanners')),
        (POTIONMAKERS, _('Potion Makers')),
        (SPELLMASTERS, _('Spell Masters')),
    ]
    title = models.CharField(max_length=250, verbose_name=_('Heading'))
    text = HTMLField(verbose_name=_('Content'))
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, verbose_name=_('Category'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('Author'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Published at'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])
