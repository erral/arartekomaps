from django.contrib import admin
from arartekomaps.places.models import Place, Access, Biblio, Bibtopic, Bibservice, MPhoto
from arartekomaps.categories.models import Category
from django import forms
from django.template.loader import render_to_string
from django.contrib.comments import Comment
from django.http import HttpResponse
from django.template import loader, Context

class AccessInline(admin.TabularInline):
    model = Access
    extra = 1
    
class BiblioInline(admin.TabularInline):
    model = Biblio
    extra = 1
    inlines = [ Bibtopic,Bibservice]

class BibtopicInline(admin.TabularInline):
    model = Bibtopic
    extra = 1

class BibserviceInline(admin.TabularInline):
    model = Bibservice
    extra = 1

class mapWidgetP(forms.widgets.Input):
    """ """
    input_type = None
    def render(self, name, value, attrs=None):
        return render_to_string('mapwidgetp.html', locals())

class PlaceAdminForm(forms.ModelForm):
    map = forms.CharField(widget=mapWidgetP(), required=False) 
    class Meta:
        model = Place
        
def export_excel(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=map_export.csv'
    places = queryset
    t = loader.get_template('csv_export.txt')
    c = Context({
        'places': places,
    })
    response.write(t.render(c))
    return response
export_excel.short_description = 'Exportar a Excel'

def export_excel_comments(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=map_export_comments.csv'
    places = []
    for place in queryset:
        coms = Comment.objects.filter(object_pk = place.id)
        if len(coms)>0:
            places.append(place)
    t = loader.get_template('csv_export_comments.txt')
    c = Context({
        'places': places,
    })
    response.write(t.render(c))
    return response
export_excel_comments.short_description = 'Exportar comentarios'

class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ('name','city','category','source')
    readonly_fields = ()
    search_fields = ('name',)
    inlines = [AccessInline, BiblioInline]
    list_filter = ('category','source', 'city')
    actions = [export_excel,export_excel_comments]
admin.site.register(Place, PlaceAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    readonly_fields = ()
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

class BibtopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ()
    search_fields = ('name',)
admin.site.register(Bibtopic, BibtopicAdmin)

class BibserviceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ()
    search_fields = ('name',)
admin.site.register(Bibservice, BibserviceAdmin)

class MPhotoAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(MPhoto,MPhotoAdmin)



