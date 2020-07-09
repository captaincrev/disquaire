from django.contrib import admin
from .models import Booking, Contact, Album, Artist
from django.utils.safestring import mark_safe
from django.urls import reverse

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'contacted']
    readonly_fields = ["created_at", "contact",'album_link', 'contacted']
    def album_link(self, booking):
        path = "admin:store_album_change"
        url = reverse(path, args=(booking.album.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

    album_link.short_description = "Album"


class BookingInline(admin.TabularInline):
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"
    model = Booking
    readonly_fields = ["created_at", "contacted", "album"]
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline,] # list of bookings made by a contact

class AlbumArtistInline(admin.TabularInline):
    verbose_name = "Disque"
    verbose_name_plural = "Disques"
    model = Album.artists.through  # the query goes through an intermediate table.
    extra = 0

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
