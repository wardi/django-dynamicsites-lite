django.dynamicsites = {
    domainToFolderName: function() {
        var domain = django.jQuery('#id_domain').val();
        if (domain) {
            return this.folderNameCheck = domain.toLowerCase().replace(/[\s\-.]/g,'_').replace(/[^a-z0-9_]/g,'');
        }
        return '';
    },
    folderNameCheck: '',
}

django.jQuery(document).ready(function() {
    var domainEl = django.jQuery('#id_domain');
    var folderNameEl = django.jQuery('#id_folder_name');
    django.dynamicsites.domainCheck = domainEl.val();
    django.dynamicsites.folderNameCheck = folderNameEl.val();
    if (django.dynamicsites.domainToFolderName() != folderNameEl.val()) {
        django.dynamicsites.folderNameEdited = true;
    }
    
    // Mark folder name as having been edited when its changed.
    folderNameEl.change(function() {
        // If the name is the same as the transformed domain, assume the
        // user did not edit the field, otherwise assume it was.
        if (folderNameEl.val() != django.dynamicsites.domainToFolderName()) {
            django.dynamicsites.folderNameEdited = true;
        }
    });
    
    // If the folder name has not been edited, auto-generate folder name from
    // domain name as a convenience.
    if (!django.dynamicsites.folderNameEdited) {
        domainEl.change(function() {
            var folder_name = folderNameEl.val();
            // If the folder name has not been edited, then set to transformed
            // domain.
            if (!django.dynamicsites.folderNameEdited) {
                folderNameEl.val(django.dynamicsites.domainToFolderName());
            }
        });
    }
});
