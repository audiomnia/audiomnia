$( function() {
  $.widget( "custom.catcomplete", $.ui.autocomplete, {
    _create: function() {
      this._super();
      this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
    },
    _renderMenu: function( ul, items ) {
      var that = this,
        currentCategory = "";
      $.each( items, function( index, item ) {
        var li;
        if ( item.category != currentCategory ) {
          ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
          currentCategory = item.category;
        }
        li = that._renderItemData( ul, item );
        if ( item.category ) {
          li.attr( "aria-label", item.category + " : " + item.label );
        }
      });
    }
  });

  var autocompleteCreators = macaulayMedia
    .map((f) => f.properties.creator)
    .reduce(function(p, c) { if (p.indexOf(c) < 0) p.push(c); return p; }, [])
    .map((c) => { return { label: c, category: "Creator" }})
    .sort()

  var autocompleteSpecies = macaulayMedia
    .map((f) => f.properties.commonName + " " + f.properties.sciName)
    .reduce(function(p, c) { if (p.indexOf(c) < 0) p.push(c); return p; }, [])
    .map((c) => { return { label: c, category: "Species" }})
    .sort()

  $( "#search" ).catcomplete({
    delay: 0,
    source: [].concat(autocompleteCreators, autocompleteSpecies)
  });
} );
