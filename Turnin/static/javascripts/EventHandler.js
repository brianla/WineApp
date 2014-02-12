
// Login Methods
$(function()
{
    // Edit the user's account
    $('#editAccountButton').bind('click', function()
    {
        var encounteredError = false;

        var currPass = $('input[name="current_password"]').val();
        var pass1 = $('input[name="edit_password"]').val();
        var pass2 = $('input[name="edit_repassword"]').val();
        var name = $('input[name="edit_name"]').val();
        var location = $('input[name="edit_location"]').val();
        var birfday = $('input[name="edit_birthday"]').val();

        //Make sure required values are not empty
        if(currPass == '' || currPass.length < 6 || currPass.length > 255) {
            $('#bold-required').css("display", 'block');
            encounteredError = true;
        } else {
            $('#bold-required').css("display", 'none');
        }

        //MAKE SURE PASSWORDS MATCH
        if( (pass1 != '' || pass2 != '') && pass1 != pass2) {
            $('#editMismatchMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#editMismatchMessage').css("display", 'none');
        }

        //Make sure new password is valid
        if( pass1 != '' && (pass1.length < 6 || pass1.length > 255 || (/[^0-9A-Za-z]/i).test(pass1)) ) {
            $('#badNewPasswordMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badNewPasswordMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( name != '' && (name.length < 2 || name.length > 255 || (/[^0-9A-Za-z\s]/).test(name)) ) {
            $('#badNewNameMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badNewNameMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( location != '' && (location.length < 2 || location.length > 255 || (/[^0-9A-Za-z\s]/).test(location)) ) {
            $('#badNewLocationMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badNewLocationMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( birfday != '' && (birfday.length < 10 || birfday.length > 10 || !(/^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])/).test(birfday)) ) {
            $('#badNewBirthdayMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badNewBirthdayMessage').css("display", 'none');
        }

        //If we had an error there is no point in continuing
        if(encounteredError)
            return false;

        //Post Account Into to Server for Account Creation
        $.post('/User/verifedit',
        {
            email    :  '{{ user.emailAddress }}',
            password :  $('input[name="current_password"]').val()
        }, function(data)
        {
            if(data.status == 'INVALID') {
                $('#editErrorMessage').css("display", 'block');
            }else if(data.status == 'VALID'){
                $('#editErrorMessage').css("display", 'none');
                $('.progress_wheel').css("display", 'block');
                $('form#editForm').submit()
                //window.location.href = data.newurl;
            }
        }, 'json');

        return false;

    });

    // Allow a user to delete their account

    $('#deleteAccountYes').bind('click', function()
    {
        $.post('/User/delete',
        {
            email    :  '{{ user.emailAddress }}'
        }, function(data)
        {
            if(data.status == 'VALID') {
                $('#deleteErrorMessage').css("display", 'none');
                window.location.href = data.newurl;
            }else{
                $('#deleteErrorMessage').css("display", 'block');
            }
        }, 'json');
    });
});


//Fix the closing of modals
$('div').each(function() {
    if(!!$(this).attr('data-reveal-id')) {
        $(this).bind('click', function(){
            var revealID = $(this).attr('data-reveal-id');
            modalwatch(function () {
                $('.reveal-modal:not(#' + revealID + ')').css('visibility', 'hidden');
                $('.reveal-modal:not(#' + revealID + ')').css('display', 'none');
            }, 1000);
        });
    }
});

$(function()
{
    // Allow the user to login
    $('#loginButton').bind('click', function()
    {
        var encounteredError = false;

        var email = $('input[name="login_email"]').val();
        var pass = $('input[name="login_password"]').val();

        //Make sure required values are not empty
        if(email == '' || email.length < 6 || email.length > 255) {
            $('#loginErrorMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#loginErrorMessage').css("display", 'none');
        }

        //Make sure required values are not empty
        if(pass == '' || pass.length < 6 || pass.length > 255) {
            $('#loginErrorMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#loginErrorMessage').css("display", 'none');
        }

        //If we had an error there is no point in continuing
        if(encounteredError)
            return false;

        $.post('/User/veriflogin',
        {
            email   :  email,
            password  :  pass
        }, function(data)
        {
            if(data.status == 'INVALID') {
                $('#loginErrorMessage').css("display", 'block');
            }else if(data.status == 'VALID'){
                $('#loginErrorMessage').css("display", 'none');
                $('form#loginForm').submit()
                //window.location.href = data.newurl;
            }
        }, 'json');
        return false;

    });
});


$(function()
{
    // Allow the user to create an account
    $('#createAccountButton').bind('click', function()
    {
        var email = $('input[name="create_email"]').val();
        var pass1 = $('input[name="create_password"]').val();
        var pass2 = $('input[name="create_repassword"]').val();
        var name = $('input[name="create_name"]').val();
        var location = $('input[name="create_location"]').val();
        var birfday = $('input[name="create_birthday"]').val();

        var encounteredError = false;

        //Make sure required values are not empty
        if(email == '' || pass1 == '' || pass2 == '') {
            $('#bold-required').css("display", 'block');
            return false;
        } else {
            $('#bold-required').css("display", 'none');
        }

        //MAKE SURE PASSWORDS MATCH
        if(pass1 != pass2) {
            $('#createMismatchMessage').css("display", 'block');
            return false;
        } else {
            $('#createMismatchMessage').css("display", 'none');
        }

        //Make sure new password is valid
        if( (pass1.length < 6 || pass1.length > 255 || (/[^0-9A-Za-z]/i).test(pass1)) ) {
            $('#badPasswordMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badPasswordMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( name != '' && (name.length < 2 || name.length > 255 || (/[^0-9A-Za-z\s]/).test(name)) ) {
            $('#badNameMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badNameMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( location != '' && (location.length < 2 || location.length > 255 || (/[^0-9A-Za-z\s]/).test(location)) ) {
            $('#badLocationMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badLocationMessage').css("display", 'none');
        }

        //Make sure name is proper length
        if( birfday != '' && (birfday.length < 10 || birfday.length > 10 || !(/^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])/).test(birfday)) ) {
            $('#badBirthdayMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badBirthdayMessage').css("display", 'none');
        }

        //If we had an error there is no point in continuing
        if(encounteredError)
            return false;

        //Post Account Into to Server for Account Creation
        $.post('/User/verifcreate',
        {
            email   :  $('input[name="create_email"]').val()
        }, function(data)
        {
            if(data.status == 'INVALID') {
                $('#createErrorMessage').css("display", 'block');
            }else if(data.status == 'VALID'){
                $('#createErrorMessage').css("display", 'none');
                $('.progress_wheel').css("display", 'block');
                $('form#createForm').submit()
                //window.location.href = data.newurl;
            }
        }, 'json');

        return false;

    });
});

// Utility Functions

function arrRmvAll(array, item) {
    for(var i = array.length; i >= 0; i--) {
        if(array[i] === item) {
            array.splice(i, 1);
        }
    }
}

// Isotopes Javascript

$(function()
{
    //Preps the Inventory layout
    var $inventory = $('#inventory_container');
    $inventory.isotope({ layoutMode : 'masonry' });
    $inventory.isotope({
        masonry: {
            columnWidth: 159
        }
    });
    $inventory.isotope({ filter: '*' });



    //Preps the Filter/s layout
    var $filter = $('#filter_container');
    $filter.isotope({ layoutMode : 'fitRows' });
    $filter.isotope({ sortBy: 'random' });
    $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-tag' });

    var imgCnt = 14;

    var adjs = new Array();
    adjs[0] = 'Terrible';
    adjs[1] = 'Radical';
    adjs[2] = 'Wicked';
    adjs[3] = 'TripleKill';
    adjs[4] = 'Gnarly';
    adjs[5] = 'Rockin';
    adjs[6] = 'Swaggin';

    //Darkens or Lightens a hex color by the given percent
    function shadeColor(color, percent) {
        var num = parseInt(color.slice(1),16), amt = Math.round(2.55 * percent), R = (num >> 16) + amt, B = (num >> 8 & 0x00FF) + amt, G = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (B<255?B<1?0:B:255)*0x100 + (G<255?G<1?0:G:255)).toString(16).slice(1);
    }

    var typewatch = (function()
    {
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        }  
    })();



    var typewatch2 = (function()
    {
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        }  
    })();


    var searchwatch = (function()
    {
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        }  
    })();


    var modalwatch = (function()
    {
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        }  
    })();

    //Forces JQuery to return hex values for BG color instead of RGB
    $.cssHooks.backgroundColor = {
        get: function(elem) {
            if (elem.currentStyle)
                var bg = elem.currentStyle["backgroundColor"];
            else if (window.getComputedStyle)
                var bg = document.defaultView.getComputedStyle(elem, null).getPropertyValue("background-color");
            if (bg.search("rgb") == -1)
                return bg;
            else {
                bg = bg.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
                function hex(x) {
                    return ("0" + parseInt(x).toString(16)).slice(-2);
                }
                return "#" + hex(bg[1]) + hex(bg[2]) + hex(bg[3]);
            }
        }
    }

    function rgbToHex(bg) {
        if (bg.search("rgb") == -1)
            return bg;
        else {
            bg = bg.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
            function hex(x) {
                return ("0" + parseInt(x).toString(16)).slice(-2);
            }
            return "#" + hex(bg[1]) + hex(bg[2]) + hex(bg[3]);
        }
    }




    //Set up the random colors for Filtering objects
    var colors = new Array();
    colors[0] = '#7E2548';
    colors[1] = '#6E1953';
    colors[2] = '#64184C';
    colors[3] = '#571542';
    colors[4] = '#48163E';


    /*Randomize bg color for filter objects*///.filter-obj:not(.filter-label, .filter-welcome)
    $( ".filter-3, .filter-tag" ).each(function() {
        $(this).css("background-color", colors[Math.floor(Math.random() * colors.length)]);
    });


    //Configures the possible sorting methods
    $('#filter_container').isotope({
        getSortData : {
            index : function ( $elem ) {
                return $elem.index();
            },
            order : function ( $elem ) {
                return parseInt( $elem.attr('order') );
            }
        }
    });

    // filter down to items of a single border color
    $('#filter_nav ul li').click(function(){
        var f = $(this).attr('filter');
        var s = $(this).attr('sortby');
        $filter.isotope({ sortBy: s });
        $filter.isotope({ filter: f });
        return false;
    });

    document.showWelcomeMsg = true;
    document.finishedLayout = false;
    //Auto-arranges the filters on mouseenter, and explodes on mouseleave
    $('#filter_container').mouseenter(function() {
        if(!document.finishedLayout) {
            $filter.isotope({ sortBy: 'index' });
            $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-obj-add, .filter-tag, .filter-label' });
            document.showWelcomeMsg = false;
            document.finishedLayout = true;
        }
    }).mouseleave(function() {
    });

    //Dynamically highlights the filter objects (if it is not activated)
    $(".filter-3, .filter-tag").mouseenter(function() {
        if(!$(this).hasClass('activated')) {
            var bgcolor = rgbToHex($(this).css("background-color"));
            var shade = shadeColor(bgcolor, 10);
            $(this).css("background-color", shade);
        }
    }).mouseleave(function() {
        if(!$(this).hasClass('activated')) {

            var bgcolor = rgbToHex($(this).css("background-color"));
            var shade = shadeColor(bgcolor, -10.1);
            $(this).css("background-color", shade);
        }
    });


    //Show edit buttons on location tiles
    //Dynamically highlights the filter objects (if it is not activated)
    $(".filter-2").mouseenter(function() {
        $('.filter-location-menu[filterKey="' + $(this).attr('filterKey') + '"]').css("display", 'block');
    }).mouseleave(function() {
        $('.filter-location-menu[filterKey="' + $(this).attr('filterKey') + '"]').css("display", 'none');
    });

    //Lays out the inventory in grid mode
    $('.filter-location-edit').click(function(){
        var locID = $(this).parent().attr('filterKey');
        var locName = $(this).parent().attr('locationName');

        $('#editLocationNumber').text(locID);
        $('#editLocationName').text(locName);
        $('input[name="editLocationNumber"]').val(locID);
        $('input[name="editLocationName"]').val(locName);
        $('#editLocationModal').foundation('reveal', 'open');

        return false;
    });

    //Lays out the inventory in grid mode
    $('.filter-location-delete').click(function(){
        var locID = $(this).parent().attr('filterKey');

        $('#deleteLocationNumber').text(locID);
        $('#deleteLocationModal').foundation('reveal', 'open');

        return false;
    });

    //Lays out the inventory in grid mode
    $('#grid_display').click(function(){
        $( ".inventory-obj" ).each(function() {
            if($(this).hasClass('inventory-1')) {
                $(this).removeClass('inventory-1');
            }
            if(!$(this).hasClass('inventory-4')) {
                $(this).addClass('inventory-4');
            }
        });
        $('.inventory-obj-info').css('display','none');
        $('.inventory-obj-add-label').css('display','none');
        $('.inventory-obj-add').css('display','block');
        $inventory.isotope('reLayout', null);
    });

    //Lays out the inventory in grid mode
    $('#list_display').click(function(){
        $( ".inventory-obj" ).each(function() {
            if($(this).hasClass('inventory-4')) {
                $(this).removeClass('inventory-4');
            }
            if(!$(this).hasClass('inventory-1')) {
                $(this).addClass('inventory-1');
            }
        });
        $('.inventory-obj-info').css('display','block');
        $('.inventory-obj-add-label').css('display','block');
        $('.inventory-obj-add').css('display','none');
        $inventory.isotope('reLayout', null);
    });


    //FILTER DIS AWWWWW YEEAAAHH
    document.filterList = new Array();


    document.filterInventoryFunction = function() {
        if($(this).attr('data-reveal-id') == 'addWineModal')
            return true;
    //if(document.filterList.length == 0)
    //return true;

    var found = false;
    var foundSearch = false;;
    var fil;
    var searchValue = $('#inventorySearch').val().toLowerCase();

    if(searchValue != '') {
        $.each(this.attributes, function(i, attrib) {
            var name = attrib.name;
            var value = attrib.value.toLowerCase();
            if (searchValue == '' || value.indexOf(searchValue) > -1) {
                foundSearch = true;
                return;
            }
        });
    }else{
        foundSearch = true;
    }

    if(document.filterList.length == 0) {
        return foundSearch;
    }


    for(var i = 0; i < document.filterList.length; i++)
    {
        found = false;
        fil = document.filterList[i].toLowerCase();
        $.each(this.attributes, function(i, attrib) {
            var name = attrib.name;
            var value = attrib.value.toLowerCase();
            if(value == fil || ((name == 'wine-tags' || name == 'user-tags') && value.indexOf(fil) > -1) ) 
            {
                found = true;
                return;
            }
        });
        if(!found)
            return false;
    }

    return foundSearch && found;
}

document.filterFiltersFunction = function() {
    if($(this).hasClass('filter-label') || $(this).hasClass('activated'))
        return true;
    var filter = $(this).attr('filterKey');

    if(!filter)
        return false;

    var tempFilterList = document.filterList.slice(0);

    tempFilterList.push(filter);

    var visibleCount = 0;


    $('.inventory-obj:not([data-reveal-id="addWineModal"])').each(function(){
        if($(this).attr('data-reveal-id') == 'addWineModal') {
            return true;
        }

        var found = false;
        var foundSearch = false;;
        var fil;
        var searchValue = $('#inventorySearch').val().toLowerCase();

        if(searchValue != '') {
            $.each(this.attributes, function(i, attrib) {
                var name = attrib.name;
                var value = attrib.value.toLowerCase();
                if (searchValue == '' || value.indexOf(searchValue) > -1) {
                    foundSearch = true;
                    return;
                }
            });
        }else{
            foundSearch = true;
        }

        if(tempFilterList.length == 0) {
            if(foundSearch)
                visibleCount++;
            return foundSearch;
        }


        for(var i = 0; i < tempFilterList.length; i++)
        {
            found = false;
            fil = tempFilterList[i].toLowerCase();
            $.each(this.attributes, function(i, attrib) {
                var name = attrib.name;
                var value = attrib.value.toLowerCase();
                if(value == fil || ((name == 'wine-tags' || name == 'user-tags') && value.indexOf(fil) > -1) ) 
                {
                    found = true;
                    return;
                }
            });
            if(!found){
                return false;
            }else{

            }
        }

        if(foundSearch && found)
            visibleCount++;
    });


if(visibleCount > 0)
    return true;
return false;
                    //});
}

    //onClick filter magic
    $('.filter-obj:not(.filter-label)').click(function() {

        //add/remove filters and update coloring
        if($(this).hasClass('activated')) {
            $(this).removeClass('activated');
            //remove filter from list
            var item = $(this).attr('filterKey');
            var index = document.filterList.indexOf(item);
            while(index != -1) {
                document.filterList.splice(index, 1);
                index = document.filterList.indexOf(item);
            }
        }else{
            $(this).addClass('activated');
            //add filter to list
            document.filterList.push($(this).attr('filterKey'));
        }

        //And update the filter :D
        $('#inventory_container').isotope({ 
            filter: document.filterInventoryFunction
        });

        if(document.filterList.length > 0) {
            $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-obj-add, .filter-tag, .filter-label, .filter-clearall' });
        }else{
            $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-obj-add, .filter-tag, .filter-label' });
        }

    });

    //Disable/Enable filter clearing
    $('.filter-clearall').click(function(){
        $('.filter-obj:not(.filter-label)').each(function() {

        //add/remove filters and update coloring
        if($(this).hasClass('activated')) {
            $(this).removeClass('activated');
                //remove filter from list
                var item = $(this).attr('filterKey');
                var index = document.filterList.indexOf(item);
                while(index != -1) {
                    document.filterList.splice(index, 1);
                    index = document.filterList.indexOf(item);
                }
            }
        });

        return false;
    });
    


    //Search For values
    $('#inventorySearch').keyup(function () {
        searchwatch(function () {
            $('#inventory_container').isotope({ 
                filter: document.filterInventoryFunction
            });
            // executed only 500 ms after the last keyup event.
        }, 400);
    });




    var activeItems = new Array();
    var pagination = new Array();
    var currentPage = 1;
    var perPageCount = 30;




    function calculateActiveItems()
    {
        //
    }

    function paginateActive()
    {
        //Adds a special class to each active item based on pagination rules
    }

    function depaginateActive()
    {
        //Removes pagination classes from active items
    }

    function calculatePaginationArray()
    {
        //includes -1 as off switch, make sure to show on page bar
    }

    function performFilter()
    {
        //Performs filtering with the given data set
    }

    function rebuildFilters()
    {
        //Clears pagination, active
        //performs filtering
        //calcaltes active
        //calcualtes pagination
    }

    function changeToPage(pageNum)
    {

    }

    function addToFilter(str)
    {
        //Adds to the filter list
        //rebuild
    }

    function removeFromFilter(str)
    {

    }

    // filter to previous page
    $('#prev_btn').click(function()
    {
     if(pagenum > 1) {
         $container.isotope({ filter: '.page' + (--pagenum) });
     }
     return false;
 });

    // filter to next page
    $('#next_btn').click(function() {
        if(pagenum < pagemax) {
            $container.isotope({ filter: '.page' + (++pagenum) });
        }
        return false;
    });

    // filter down to items of a single border color

    $('#filters div').click(function() {
        var selector = $(this).attr('filter');
        $container.isotope({ filter: selector });
        return false;
    });



    //Add wine AJAX
    $(function()
    {
        $('#addWineButton').bind('click', function()
        {


            var qualityStr = $('input[name="quality"]').val();
            var qualityArr = qualityStr.split(",");
            //Post Wine to Inventory
            $.post('/Inventory/verifAddWine',
            {
                email           :  '{{ user.emailAddress }}',
                wineName        :  $('input[name="wineName"]').val(),
                wineLocation    :  $('#locationDropDown').val(),
                winery          :  $('input[name="winery"]').val(),
                region          :  $('input[name="region"]').val(),
                varietal        :  $('input[name="varietal"]').val(),
                vintage         :  $('input[name="vintage"]').val(),
                quantity        :  $('input[name="quantity"]').val(),
                rating          :  $('input[name="rating"]').val(),
                quality         :  $('input[name="quality"]').val(),//JSON.stringify(qualityArr),
                description     :  $('textarea[name="description"]').val(),
                wishList        :  $('input[name="wishList"]').is(':checked')
            }, function(data)
            {
                if(data.status == 'INVALID') {
                    $('#createErrorMessage').css("display", 'block');
                }else if(data.status == 'VALID'){
                    $('#createErrorMessage').css("display", 'none');
                    $('.progress_wheel').css("display", 'block');
                    $('form#addWineForm').submit()
                    //window.location.href = data.newurl;

                    //Close modal
                    $('#addWineModal').foundation('reveal','close');
                }
            }, 'json');

return false;

});
});

//Edit wine AJAX
$(function()
{
    $('#editWineButton').bind('click', function()
    {

        $('.progress_wheel').css("display", 'block');
        $('form#editWineForm').submit();
        //window.location.href = data.newurl;

        //Close modal
        $('#editWineModal').foundation('reveal','close');

        return false;

    });
});

    // Delete wine
    $(function()
    {
        $('#deleteWineYes').bind('click', function()
        {
            $.post('/Inventory/deleteWine',
            {
                li_wineID       :  $('#wineInfoModal').attr('wine-wineID'),
                li_locationID   :  $('.inventory-obj[wine-wineID="' + $('#wineInfoModal').attr('wine-wineID') + '"]').attr('user-li-locationID')

            }, function(data)
            {
                if(data.status == 'INVALID') {
                    $('#createErrorMessage').css("display", 'block');
                }else if(data.status == 'VALID'){
                    $('#createErrorMessage').css("display", 'none');
                    $('.progress_wheel').css("display", 'block');

                //Close modal
                $('#deleteWineModal').foundation('reveal','close');

                //Reload page
                location.reload(false);
            }

        }, 'json');

            return false;
        });
    });

//Edit wine AJAX
$(function()
{
    $('#addLocationButton').bind('click', function()
    {
        $('form#addLocationForm').submit();
        //Close modal
        $('#addLocationModal').foundation('reveal','close');

        return false;

    });
});

//Display wine info
$(function()
{
    $('[data-reveal-id="wineInfoModal"]').bind('click', function()
    {

        var viewWineModal = $('#wineInfoModal');
        var staticPath = '{{ url_for('static', filename='images/wine/') }}';

        $('#wineInfoModal').attr('wine-wineID', $(this).attr('wine-wineID'));
        $('#wine_wineName').text($(this).attr('wine-wineName'));
        $('#wine_winery').text($(this).attr('wine-winery'));
        $('#wine_varietal').text($(this).attr('wine-varietal'));
        if($(this).attr('wine-vintage') === '0')
            $('#wine_vintage').text('Blend');
        else 
            $('#wine_vintage').text($(this).attr('wine-vintage'));
        $('#wine_averageStarRating').text($(this).attr('wine-averageStarRating'));
        $('#wine_region').text($(this).attr('wine-region'));
        $('#user_quantity').text($(this).attr('user-quantity'));
        $('#user_tags').text($(this).attr('user-tags'));
        $('#user_description').text($(this).attr('user-description'));
        $('#user_isWishlist').text($(this).attr('user-isWishlist'));
        $('#user_personalStarRating').text($(this).attr('user-personalStarRating'));

        //Image fall-back code
        var imagePath = $(this).attr('user-imagePath');
        if(imagePath == null || imagePath == '' || imagePath == 'None')
            imagePath = $(this).attr('wine-imagePath');
        if(imagePath == null || imagePath == '' || imagePath == 'None')
            imagePath = 'default_wine.jpg';
        $('#user_imagePath').attr('src', staticPath + imagePath);

        $('#wineInfoModal').foundation('reveal', 'open');

        return false;

    });
});

$(function() {
    $('[data-reveal-id="editWineModal"]').bind('click', function()
    {
        $('#addWineModal').foundation('reveal', 'open');
                    //$('#massive-container').isotope({ filter: '.special_iso_right' });
                });
});

//Edit a wine
$(function()
{
    $('[data-reveal-id="editWineModal"]').bind('click', function()
    {

        var viewWineModal = $('#editWineModal');
        var staticPath = '{{ url_for('static', filename='images/wine/') }}';
        var wineID = $('#wineInfoModal').attr('wine-wineID');


        $('[name="edit_wineID"]').val(wineID);
        $('[name="edit_wineName"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-wineName'));
        $('[name="original_wineLocation"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-li-locationID'));
        $('[name="edit_winery"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-winery'));
        $('[name="edit_varietal"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-varietal'));
        $('[name="edit_vintage"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-vintage'));
        $('[name="edit_averageStarRating"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-averageStarRating'));
        $('[name="edit_region"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('wine-region'));
        $('[name="edit_quantity"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-quantity'));
        $('[name="edit_quality"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-tags'));
        $('[name="edit_description"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-description'));
        $('[name="edit_isWishlist"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-isWishlist'));
        $('[name="edit_personalStarRating"]').val($('.inventory-obj[wine-wineID="' + wineID + '"]').attr('user-personalStarRating'));


        $('#editWineModal').foundation('reveal', 'open');

        return false;

    });
});

$(function()
{
    $('[data-reveal-id="deleteWineModal"]').bind('click', function()
    {

        $('#deleteWineModal').foundation('reveal', 'open');

        return false;

    });
});

//Make Ajax Request for Candidate Wines
//This will only fire after a keyboard event has occurred on one of the search boxes AND
//a certain delay has passed.  Each new keyboard even refreshes the delay.

$('.autocompleteTextField').keyup(function () {
    typewatch(function () {

        $.post('/Recommend/candidateWines',
        {
            //Create a dictionary that has the current search terms
            wineName   :   $('input[id="autocomplete1"]').val(),
            winery     :   $('input[id="autocomplete2"]').val(),
            vintage    :   $('input[id="autocomplete3"]').val()
        }, function(data)
        {


            if(data.status == 'INVALID') {
                //alert('IT R BROKE K?');
                //Clear the candidate list
                $('#candyWineList').empty();
            }else if(data.status == 'VALID'){



                //Clear the candidate list
                $('#candyWineList').empty();


                //For each candidate, build a div and add an on click listener
                var cand;
                for(var i = 0; i < data.candidates.length; i++) {
                    cand = data.candidates[i];

                    //Construct a massiv div with all of the candidate wine's info and append it to the end of the #candyWineList
                    $('#candyWineList').append('<div class="row candidate-wine-holder" ' +
                        'wineID="' + cand.wineID + '" ' +
                        'wineName="' + cand.wineName + '" ' +
                        'winery="' + cand.winery + '" ' +
                        'vintage="' + cand.vintage + '" ' +
                        'varietal="' + cand.varietal + '" ' +
                        'wineType="' + cand.wineType + '" ' +
                        'region="' + cand.region + '" ' +
                        'tags="' + cand.tags + '" ' +
                        'description="' + cand.description + '" ' +
                        'averageStarRating="' + cand.averageStarRating + '" ' +
                        'imagePath="' + cand.imagePath + '" ' +
                        'bitter="' + cand.bitter + '" ' +
                        'sweet="' + cand.sweet + '" ' +
                        'sour="' + cand.sour + '" ' +
                        'salty="' + cand.salty + '" ' +
                        'chemical="' + cand.chemical + '" ' +
                        'pungent="' + cand.pungent + '" ' +
                        'oxidized="' + cand.oxidized + '" ' +
                        'microbiological="' + cand.microbiological + '" ' +
                        'floral="' + cand.floral + '" ' +
                        'spicy="' + cand.spicy + '" ' +
                        'fruity="' + cand.fruity + '" ' +
                        'vegetative="' + cand.vegetative + '" ' +
                        'nutty="' + cand.nutty + '" ' +
                        'caramelized="' + cand.caramelized + '" ' +
                        'woody="' + cand.woody + '" ' +
                        'earthy="' + cand.earthy + '" ' +
                        '><div class="large-12 columns candidate-wine">' + cand.vintage + ' ' + cand.winery + '\'s ' + cand.wineName +'</div></div>');
}

$('.candidate-wine-holder').each(function() {
    $(this).click(function() {

        //Hide the candidate list
        $('.special_iso_left').css('display', 'none');

        //Fill out form values
        $('[name="wineID"]').val($(this).attr('wineID'));
        $('[name="wineName"]').val($(this).attr('wineName'));
        $('[name="winery"]').val($(this).attr('winery'));
        $('[name="varietal"]').val($(this).attr('varietal'));
        $('[name="vintage"]').val($(this).attr('vintage'));
        $('[name="region"]').val($(this).attr('region'));
        $('[name="quantity"]').val($(this).attr('quantity'));
        $('[name="quality"]').val($(this).attr('tags'));
        $('[name="description"]').val($(this).attr('description'));
        $('[name="isWishlist"]').val($(this).attr('isWishlist'));
        $('[name="personalStarRating"]').val($(this).attr('personalStarRating'));
        
    });
});


}

}, 'json');
                    // executed only 500 ms after the last keyup event.
                }, 500);
});

    //Delete Location
    $('#deleteLocationYes').bind('click', function()
    {
        $.post('/Inventory/deleteInventory',
        {
            email    :  '{{ user.emailAddress }}',
            locationID : $('#deleteLocationNumber').text()
        }, function(data)
        {
            if(data.status == 'VALID') {
                $('#deleteLocationErrorMessage').css("display", 'none');
                location.reload(false);
            }else{
                $('#deleteLocationErrorMessage').css("display", 'block');
            }
        }, 'json');
    });



    //Edit Location
    $('#editLocationButton').bind('click', function()
    {
        $('form#editLocationForm').submit();

    });


    //Finally show the inventory
    $('#progress_wheel_container').css("display", 'none');
    $('#inventory_container').css("display", 'block');
    $('#filter_container').css("display", 'block');

    //Preps the Inventory layout
    $inventory.isotope({ layoutMode : 'masonry' });
    $inventory.isotope({ filter: '*' });

    typewatch2(function () {
        //Fix for chrome
        if({% if not fullLocations or fullLocations|count == 0 %} {{ 'true' }} {% else %} {{ 'false' }} {% endif %})
        {
            $inventory.isotope({ filter: '.inventory-obj:not(.inventory-obj[data-reveal-id="addWineModal"])' });
        }else {
            $inventory.isotope({ filter: '*' });
        }
        $inventory.isotope({ layoutMode : 'masonry' });
    }, 1500);


    typewatch(function () {
        if(!document.finishedLayout){
            $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-tag' });
        }
        typewatch(function () {
            if(document.showWelcomeMsg)
            {
                $filter.isotope({ sortBy: 'index' });
                $filter.isotope({ filter: '*' });
                typewatch(function () {
                    $filter.isotope({ sortBy: 'index' });
                    $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-obj-add, .filter-tag, .filter-label' });
                    document.finishedLayout = true;
                }, 5000);
            }
        }, 1500);
    }, 200);



    //Preps the Filter/s layout
    $filter.isotope({ layoutMode : 'fitRows' });
    $filter.isotope({ sortBy: 'random' });
    $filter.isotope({ filter: '.filter-2, .filter-3, .filter-4, .filter-tag' });


    if({% if not fullLocations or fullLocations|count == 0 %} {{ 'true' }} {% else %} {{ 'false' }} {% endif %})
    {
        $inventory.isotope({ filter: '.inventory-obj:not(.inventory-obj[data-reveal-id="addWineModal"])' });
        $filter.isotope({ sortBy: 'index' });
        $filter.isotope({ filter: '*' });
    }


    


    $('#three_d_display').bind('click', function() {
        $('#threeDModal').foundation('reveal', 'open');
        load3DModal();
    });

    var table = [
    {% for wine in inventory %}
    {% if loop.index > 1 %}
    {{ ',' }}
    {% endif %}
    ['{{wine.wine_wineID}}',
    '{{wine.wine_wineName}}',
    '{{wine.wine_winery}}',
    '{{wine.wine_vintage}}',
    '{{wine.wine_varietal}}',
    '{{wine.wine_wineType}}',
    '{{wine.wine_region}}',
    '{{wine.wine_tags}}',
    '{{wine.wine_description}}',
    '{{wine.wine_averageStarRating}}',
    '{{wine.wine_imagePath}}',
    '{{wine.wine_bitter}}',
    '{{wine.wine_sweet}}',
    '{{wine.wine_sour}}',
    '{{wine.wine_salty}}',
    '{{wine.wine_chemical}}',
    '{{wine.wine_pungent}}',
    '{{wine.wine_oxidized}}',
    '{{wine.wine_microbiological}}',
    '{{wine.wine_floral}}',
    '{{wine.wine_spicy}}',
    '{{wine.wine_fruity}}',
    '{{wine.wine_vegetative}}',
    '{{wine.wine_nutty}}',
    '{{wine.wine_caramelized}}',
    '{{wine.wine_woody}}',
    '{{wine.wine_earthy}}',

    '{{wine.user_li_locationID}}',
    '{{wine.user_quantity}}',
    '{{wine.user_isWishlist}}',
    '{{wine.user_tags}}',
    '{{wine.user_description}}',
    '{{wine.user_personalStarRating}}',
    '{{wine.user_imagePath}}',
    '{{wine.user_bitter}}',
    '{{wine.user_sweet}}',
    '{{wine.user_sour}}',
    '{{wine.user_salty}}',
    '{{wine.user_chemical}}',
    '{{wine.user_pungent}}',
    '{{wine.user_oxidized}}',
    '{{wine.user_microbiological}}',
    '{{wine.user_floral}}',
    '{{wine.user_spicy}}',
    '{{wine.user_fruity}}',
    '{{wine.user_vegetative}}',
    '{{wine.user_nutty}}',
    '{{wine.user_caramelized}}',
    '{{wine.user_woody}}',
    '{{wine.user_earthy}}',
    {% if wine is defined and wine.user_imagePath %}
    '{{ url_for('static', filename=('images/wine/' + wine.user_imagePath) ) }}'
    {% elif wine is defined and wine.wine_imagePath %}
    '{{ url_for('static', filename=('images/wine/' + wine.wine_imagePath) ) }}'
    {% else %}
    '{{ url_for('static', filename='images/wine/default_wine.jpg' ) }}'
    {% endif %}
    ]
    {% endfor %}
    ];
    
    var camera, scene, renderer;
    var controls;
    
    var objects = [];
    var targets = { table: [], sphere: [], helix: [], grid: [] };

    var modal = document.createElement( 'div' );
    modal.id='three_d_wineInfoModal';
    modal.style.display = 'none';
    modal.innerHTML = '<div class="row">' + 
    '<div class="large-4 columns">' + 
    '<h2 id="three_d_wine_wineName">Wine Name</h2>' + 
    '<h4 id="three_d_wine_winery">Winery</h4>' + 
    '<img id="three_d_user_imagePath" src="static/images/wine/default_wine.jpg" />' + 
    '</div>' + 

    '<div class="large-8 columns">' + 
    '<div class="row">' + 
    '<div class="section-container accordion" data-section="accordion">' + 
    '<section class="section active">' + 
    '<p class="title" data-section-title>' + 
    '<a href="#">Information</a>' + 
    '</p>' + 
    '<div class="content" data-section-content>' + 
    '<p id="three_d_user_description">Description</p>' + 

    '<h3>Tags:</h3>' + 
    '<ul id="three_d_user_tags"class="tags">' + 
    '<li><div class="tag">A Tag</div></li>' + 
    '</ul>' + 
    '</div>' + 
    '</section>' + 
    '<section>' + 
    '<p class="title" data-section-title>' + 
    '<a href="#">More Info.</a>' + 
    '</p>' + 
    '<div class="content" data-section-content>' + 
    '<ul id="">' + 
    '<li><strong>Varietal:</strong><div id="three_d_wine_varietal"></div></li>' + 
    '<li><strong>Region:</strong><div id="three_d_wine_region"></div></li>' + 
    '<li><strong>Your Rating:</strong><div id="three_d_user_personalStarRating"></div></li>' + 
    '<li><strong>Average Rating:</strong><div id="three_d_wine_averageStarRating"></div></li>' + 
    '<li><strong>Quantity:</strong><div id="three_d_user_quantity"></div></li>' + 
    '<li><strong>Wishlist:</strong><div id="three_d_user_isWishlist"></div></li>' + 
    '</ul>' + 
    '</div>' + 
    '</section>' + 
    '</div>' + 
    '</div>' + 
    '</div>' + 
    '</div>' + 
    '<a class="close-reveal-modal">&#215;</a>';
    modal = new THREE.CSS3DObject( modal );


    
    function load3DModal()
    {
        if(renderer == null)
            setTimeout(function() {
               init();
               animate();
           }, 500);
        
    }
    
    function dispose3D() {
        //document.getElementById( 'container' ).removeChild( renderer.domElement );
    }
    
    function init() {

        //Prep the container for camera calculations
        var container = $("#three_d_container");
        
        camera = new THREE.PerspectiveCamera( 75, container.width() / container.height(), 1, 5000 );
        camera.position.z = 600;
        
        scene = new THREE.Scene();
        
        scene.add( modal );
        
        
        //Add a background object
        //For assisting with solving the culling bug
        var bg = document.createElement( 'div' );
        bg.className = 'bg3D';
        bg.style.backgroundColor = 'rgba(0,0,0,0.8)';
        
        var bgObj = new THREE.CSS3DObject( bg );
        bgObj.position.x = 0;
        bgObj.position.y = 0;
        bgObj.position.z = 0;
        /*scene.add( bgObj );*/
        
        
        
        for ( var i = 0; i < table.length; i ++ ) {

            var item = table[ i ];
            
            var element = document.createElement( 'div' );
            element.className = 'inventory-obj-three-d inventory-4';
            element.setAttribute('wine-wineID', item[0]); 
            element.setAttribute('wine-wineName', item[1]); 
            element.setAttribute('wine-winery', item[2]); 
            element.setAttribute('wine-vintage', item[3]); 
            element.setAttribute('wine-varietal', item[4]); 
            element.setAttribute('wine-wineType', item[5]); 
            element.setAttribute('wine-region', item[6]); 
            element.setAttribute('wine-tags', item[7]); 
            element.setAttribute('wine-description', item[8]); 
            element.setAttribute('wine-averageStarRating', item[9]); 
            element.setAttribute('wine-imagePath', item[10]); 
            element.setAttribute('wine-bitter', item[11]); 
            element.setAttribute('wine-sweet', item[12]); 
            element.setAttribute('wine-sour', item[13]); 
            element.setAttribute('wine-salty', item[14]); 
            element.setAttribute('wine-chemical', item[15]); 
            element.setAttribute('wine-pungent', item[16]); 
            element.setAttribute('wine-oxidized', item[17]); 
            element.setAttribute('wine-microbiological', item[18]); 
            element.setAttribute('wine-floral', item[19]); 
            element.setAttribute('wine-spicy', item[20]); 
            element.setAttribute('wine-fruity', item[21]); 
            element.setAttribute('wine-vegetative', item[22]); 
            element.setAttribute('wine-nutty', item[23]); 
            element.setAttribute('wine-caramelized', item[24]); 
            element.setAttribute('wine-woody', item[25]); 
            element.setAttribute('wine-earthy', item[26]); 

            element.setAttribute('user-li-locationID', item[27]); 
            element.setAttribute('user-quantity', item[28]); 
            element.setAttribute('user-isWishlist', item[29]); 
            element.setAttribute('user-tags', item[30]); 
            element.setAttribute('user-description', item[31]); 
            element.setAttribute('user-personalStarRating', item[32]); 
            element.setAttribute('user-imagePath', item[33]); 
            element.setAttribute('user-bitter', item[34]); 
            element.setAttribute('user-sweet', item[35]); 
            element.setAttribute('user-sour', item[36]); 
            element.setAttribute('user-salty', item[37]); 
            element.setAttribute('user-chemical', item[38]); 
            element.setAttribute('user-pungent', item[39]); 
            element.setAttribute('user-oxidized', item[40]); 
            element.setAttribute('user-microbiological', item[41]);
            element.setAttribute('user-floral', item[42]); 
            element.setAttribute('user-spicy', item[43]); 
            element.setAttribute('user-fruity', item[44]); 
            element.setAttribute('user-vegetative', item[45]); 
            element.setAttribute('user-nutty', item[46]); 
            element.setAttribute('user-caramelized', item[47]); 
            element.setAttribute('user-woody', item[48]); 
            element.setAttribute('user-earthy', item[49]); 

            var imageCont = document.createElement('div');
            imageCont.className = 'inventory-obj-image';

            var image = document.createElement('img');
            image.setAttribute('src', item[50]);

            imageCont.appendChild(image);
            element.appendChild(imageCont);

            
            element.addEventListener('click', function() {

                $('#three_d_wineInfoModal').attr('wine-wineID', $(this).attr('wine-wineID'));
                $('#three_d_wine_wineName').text($(this).attr('wine-wineName'));
                $('#three_d_wine_winery').text($(this).attr('wine-winery'));
                $('#three_d_wine_varietal').text($(this).attr('wine-varietal'));
                $('#three_d_wine_vintage').text($(this).attr('wine-vintage'));
                $('#three_d_wine_averageStarRating').text($(this).attr('wine-averageStarRating'));
                $('#three_d_wine_region').text($(this).attr('wine-region'));
                $('#three_d_user_quantity').text($(this).attr('user-quantity'));
                $('#three_d_user_tags').text($(this).attr('user-tags'));
                $('#three_d_user_description').text($(this).attr('user-description'));
                $('#three_d_user_isWishlist').text($(this).attr('user-isWishlist'));
                $('#three_d_user_personalStarRating').text($(this).attr('user-personalStarRating'));

                $('#three_d_user_imagePath').attr('src', item[50]);

                $('#three_d_wineInfoModal').css('display', 'block');
            });

element.addEventListener('click', function(event)
{
    var object3d = event.target, rotation, color;
    modal.lookAt( object3d.position );
});



var object = new THREE.CSS3DObject( element );

scene.add( object );                    
objects.push( object );

}

            // table
            
            for ( var i = 0; i < objects.length; i ++ ) {

                var item = table[ i ];
                
                var object = new THREE.Object3D();
                object.position.y = ( ~~(i / 4.0) * 160 ) - ((table.length-8)*160/4);
                object.position.x = - ( ~~(i % 4) * 200 ) + 300;
                
                targets.table.push( object );
                
            }
            
            // sphere
            
            var vector = new THREE.Vector3();
            
            for ( var i = 0, l = objects.length; i < l; i ++ ) {

                var phi = Math.acos( -1 + ( 2 * i ) / l );
                var theta = Math.sqrt( l * Math.PI ) * phi;
                
                var object = new THREE.Object3D();
                
                object.position.x = 800 * Math.cos( theta ) * Math.sin( phi );
                object.position.y = 800 * Math.sin( theta ) * Math.sin( phi );
                object.position.z = 800 * Math.cos( phi );
                
                vector.copy( object.position ).multiplyScalar( 20 );
                
                object.lookAt( vector );
                
                targets.sphere.push( object );
                
            }
            
            // helix
            
            var vector = new THREE.Vector3();
            
            for ( var i = 0, l = objects.length; i < l; i ++ ) {

                var phi = i * 0.175 + Math.PI;
                
                var object = new THREE.Object3D();
                
                object.position.x = 1100 * Math.sin( phi );
                object.position.y = - ( i * 8 ) + 450;
                object.position.z = 1100 * Math.cos( phi );
                
                vector.copy( object.position );
                vector.x *= 2;
                vector.z *= 2;
                
                object.lookAt( vector );
                
                targets.helix.push( object );
                
            }
            
            // grid
            
            for ( var i = 0; i < objects.length; i ++ ) {

                var object = new THREE.Object3D();
                
                object.position.x = ( ( i % 5 ) * 400 ) - 800;
                object.position.y = ( - ( Math.floor( i / 5 ) % 5 ) * 400 ) + 800;
                object.position.z = ( Math.floor( i / 25 ) ) * 1000 - 2000;
                
                targets.grid.push( object );
                
            }
            
            //
            
            var container = $("#three_d_container");
            
            renderer = new THREE.CSS3DRenderer();
            
            //This 0.8 nonsense correspondes to the 80% width/height props
            //in the iso.css file, this is a terrible fix
            renderer.setSize( 0.8*window.innerWidth/*container.width()*/, 0.8*window.innerHeight /*container.height()*/ );
            renderer.domElement.style.position = 'absolute';
            document.getElementById( 'three_d_container' ).appendChild( renderer.domElement );
            
            //
            
            controls = new THREE.TrackballControls( camera, renderer.domElement );
            controls.rotateSpeed = 0.5;
            controls.addEventListener( 'change', render );
            
            var button = document.getElementById( 'table' );
            button.addEventListener( 'click', function ( event ) {

                transform( targets.table, 2000 );

            }, false );
            
            var button = document.getElementById( 'sphere' );
            button.addEventListener( 'click', function ( event ) {

                transform( targets.sphere, 2000 );

            }, false );
            
            var button = document.getElementById( 'helix' );
            button.addEventListener( 'click', function ( event ) {

                transform( targets.helix, 2000 );

            }, false );
            
            var button = document.getElementById( 'grid' );
            button.addEventListener( 'click', function ( event ) {

                transform( targets.grid, 2000 );

            }, false );
            
            transform( targets.table, 1500 );
            //transform( targets.helix, 2000 );
            //transform( targets.sphere, 2000 );
            
            //
            
            window.addEventListener( 'resize', onWindowResize, false );
            
        }
        
        function transform( targets, duration ) {

            TWEEN.removeAll();
            
            for ( var i = 0; i < objects.length; i ++ ) {

                var object = objects[ i ];
                var target = targets[ i ];
                
                new TWEEN.Tween( object.position )
                .to( { x: target.position.x, y: target.position.y, z: target.position.z }, Math.random() * duration + duration )
                .easing( TWEEN.Easing.Exponential.InOut )
                .start();
                
                new TWEEN.Tween( object.rotation )
                .to( { x: target.rotation.x, y: target.rotation.y, z: target.rotation.z }, Math.random() * duration + duration )
                .easing( TWEEN.Easing.Exponential.InOut )
                .start();
                
            }
            
            new TWEEN.Tween( this )
            .to( {}, duration * 2 )
            .onUpdate( render )
            .start();
            
        }
        
        function onWindowResize() {

            var container = $("#three_d_container");
            
            camera.aspect = container.width() / container.height();
            camera.updateProjectionMatrix();
            
            renderer.setSize( 0.8*window.innerWidth/*container.width()*/, 0.8*window.innerHeight /*container.height()*/ );
            
        }
        
        function animate() {

            requestAnimationFrame( animate );
            
            TWEEN.update();
            controls.update();
            
        }
        
        function render() {

            renderer.render( scene, camera );
            
        }

        </script>

        <script>
        

        var final_transcript = '';
        var recognizing = false;
        var ignore_onend;
        var start_timestamp;
        if (('webkitSpeechRecognition' in window)) {
          //start_button.style.display = 'inline-block';
          var recognition = new webkitSpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = true;

          recognition.onstart = function() {
            recognizing = true;
            //showInfo('info_speak_now');
            //start_img.src = 'mic-animate.gif';
        };

        recognition.onerror = function(event) {
        };

        recognition.onend = function() {

            recognizing = false;
            if (ignore_onend) {
              return;
          }


            //start_img.src = 'mic.gif';


            if (!final_transcript) {
              //showInfo('info_start');
              alert('transcript failed?');
              return;
          }

          showInfo('');
          if (window.getSelection) {
              window.getSelection().removeAllRanges();
              var range = document.createRange();
              range.selectNode(document.getElementById('final_span'));
              window.getSelection().addRange(range);
          }
      };

      recognition.onresult = function(event) {
        var interim_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            final_transcript += event.results[i][0].transcript;
        } else {
            interim_transcript += event.results[i][0].transcript;
        }
    }

    final_transcript = capitalize(final_transcript);

    $('#inventorySearch').val(final_transcript);
    $('#inventorySearch').trigger('keyup');
            /*
            final_span.innerHTML = linebreak(final_transcript);
            interim_span.innerHTML = linebreak(interim_transcript);
            if (final_transcript || interim_transcript) {
              showButtons('inline-block');
            }
            */
        };
    }


    var two_line = /\n\n/g;
    var one_line = /\n/g;
    function linebreak(s) {
      return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
  }

  var first_char = /\S/;
  function capitalize(s) {
      return s.replace(first_char, function(m) { return m.toUpperCase(); });
  }



  function startButton(event) {
      if (recognizing) {
        recognition.stop();
        return;
    }
    final_transcript = '';
    recognition.lang = 6;
    recognition.start();
    ignore_onend = false;
    start_timestamp = event.timeStamp;
}

$('#search-by-voice').click(function()
{
 startButton(event);
 $('#search-by-voice').css('background-color', '#EEE');
 return false;
});


    //Preps the Inventory layout
    var $recommandations = $('#recommendation-container');
    $recommandations.isotope({ layoutMode : 'masonry' });
    $recommandations.isotope({
        masonry: {
            columnWidth: 232
        }
    });

    $('.channel-button:first').addClass('shelf-active');
    $recommandations.isotope({ filter: '.recommended-' + $('.channel-button:first').attr('shelf-id') });


    $('.channel-button').click(function() {

        //Filter to show just recomms from current self
        //And update the filter :D
        $('#recommendation-container').isotope({ 
            filter: ('.recommended-' + $(this).attr('shelf-id'))
        });

        $('.channel-button').removeClass('shelf-active');
        $(this).addClass('shelf-active');

    });



    $('.recommend-more').bind('click', function()
    {

        $('#progress_wheel_container').css("display", 'block');
        //Post the wineIDs
        $.post('/Recommend/getRecommendations',
        {
            recommenderID :  $('.shelf-active').attr('shelf-id')
        }, function(data)
        {
            if(data.status == 'VALID') {



                var cand;
                for(var i = 0; i < data.candidates.length; i++) {

                    cand = data.candidates[i];

                    var staticPath = '/static/images/wine/';
                    var imagePath;
                    if(cand.imagePath != null && cand.imagePath != '')
                        imagePath = cand.imagePath;
                    else
                        imagePath = 'default_wine.jpg';


                    $('#recommendation-container').prepend('<div class="recommendation-obj recommended-' + $('.shelf-active').attr('shelf-id') + '">' + 
                        '<div class="recommendation-obj-image">' + 
                        '<img src="' + staticPath + imagePath + '" />' +
                        '</div>' + 
                        '<div class="winename">' + cand.wineName + '</div>' + 
                        '<div class="winedesc">' + cand.winery + '<br />' + cand.vintage + '</div>' + 
                        '<div data-reveal-id="wineModal" class="moreinfo"' + 
                        'wine-wineID="' + cand.wineID + '" ' +
                        'wine-wineName="' + cand.wineName + '" ' +
                        'wine-winery="' + cand.winery + '" ' +
                        'wine-vintage="' + cand.vintage + '" ' +
                        'wine-varietal="' + cand.varietal + '" ' +
                        'wine-wineType="' + cand.wineType + '" ' +
                        'wine-region="' + cand.region + '" ' +
                        'user-tags="' + cand.tags + '" ' +
                        'user-description="' + cand.description + '" ' +
                        'wine-averageStarRating="' + cand.averageStarRating + '" ' +
                        'wine-imagePath="' + cand.imagePath + '" ' +
                        'bitter="' + cand.bitter + '" ' +
                        'sweet="' + cand.sweet + '" ' +
                        'sour="' + cand.sour + '" ' +
                        'salty="' + cand.salty + '" ' +
                        'chemical="' + cand.chemical + '" ' +
                        'pungent="' + cand.pungent + '" ' +
                        'oxidized="' + cand.oxidized + '" ' +
                        'microbiological="' + cand.microbiological + '" ' +
                        'floral="' + cand.floral + '" ' +
                        'spicy="' + cand.spicy + '" ' +
                        'fruity="' + cand.fruity + '" ' +
                        'vegetative="' + cand.vegetative + '" ' +
                        'nutty="' + cand.nutty + '" ' +
                        'caramelized="' + cand.caramelized + '" ' +
                        'woody="' + cand.woody + '" ' +
                        'earthy="' + cand.earthy + '">More Info</div></div>').isotope( 'reloadItems' ).isotope({ sortBy: 'original-order' });
}

bindWineModalClick();

}else{
}

$('#progress_wheel_container').css("display", 'none');
typewatch2(function () {
                        //Fix for chrome
                        $('#recommendation-container').isotope({ filter: '.recommended-' + $('.shelf-active').attr('shelf-id') });
                    }, 500);
}, 'json');
});

var modalwatch = (function()
{
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
}  
})();



$(function() {

//On click event for Create Shelf Button
$('#createShelf').bind('click', function()
{
  var children = $('#seedList').children();
  var childCount = children.length;
  var shelfName = $('input[id="shelfName"]').val();

  var encounteredError = false;

      //If we have no seeds then we can;t make a channel, throw error
      if(childCount == 0) {
        $('#badSeedMessage').css("display", 'block');
        encounteredError = true;
    } else {
        $('#badSeedMessage').css("display", 'none');
    }


        //Make sure name is proper length
        if( (shelfName.length < 2 || shelfName.length > 255 || (/[^0-9A-Za-z\s]/).test(shelfName)) ) {
            $('#badShelfNameMessage').css("display", 'block');
            encounteredError = true;
        } else {
            $('#badShelfNameMessage').css("display", 'none');
        }

        //If we had an error, bail out
        if(encounteredError)
          return false;


      //Loop through all of the seeds and add their wine IDs to an array
      var wineIDArr = Array();
      for(var i = 0; i < childCount; i++)
      {
        wineIDArr[i] = children.eq(i).attr('wineID');
    }

      //Post the wineIDs
      $.post('/Recommend/createShelf',
      {
        email     :  '{{ user.emailAddress }}',
        shelfName :  shelfName,
        seeds     :  JSON.stringify(wineIDArr)
    }, function(data)
    {
        if(data.status == 'VALID') {
            
                //Close modal
                $('#shelfModal').foundation('reveal','close');

                //Reload page
                location.reload(false);
            }else{

            }
        }, 'json');
  });


$('[data-reveal-id="edit_shelfModal"]').bind('click', function()
{
    $('#edit_shelfDropDown').trigger('change');
    $('#edit_shelfModal').foundation('reveal','close');
});

$('[data-reveal-id="inventoryModal"]').bind('click', function()
{
    $('#inventoryModal').foundation('reveal', 'open');
});




/****************************************************
EDIT SHELF COPY PASTA
******************************************************/

$('#editShelf').bind('click', function()
{
  var children = $('#edit_seedList').children();
  var childCount = children.length;
  var recID = $('select[name="edit_recommenderID"]').val();

  var encounteredError = false;

      //If we have no seeds then we can;t make a channel, throw error
      if(childCount == 0) {
        $('#edit_badSeedMessage').css("display", 'block');
        encounteredError = true;
    } else {
        $('#edit_badSeedMessage').css("display", 'none');
    }


        //If we had an error, bail out
        if(encounteredError)
          return false;


      //Loop through all of the seeds and add their wine IDs to an array
      var wineIDArr = Array();
      for(var i = 0; i < childCount; i++)
      {
        wineIDArr[i] = children.eq(i).attr('wineID');
    }

      //Post the wineIDs
      $.post('/Recommend/editShelf',
      {
        email             :  '{{ user.emailAddress }}',
        /*shelfName         :  shelfName,*/
        seeds             :  JSON.stringify(wineIDArr),
        recommenderID     :  recID
    }, function(data)
    {
        if(data.status == 'VALID') {
                //$('#deleteErrorMessage').css("display", 'none');
                
                //Close modal
                $('#edit_shelfModal').foundation('reveal','close');

                //Reload page
                location.reload(false);
            }else{
            }
        }, 'json');
  });

});


//Add wine to inventory AJAX
$(function()
{
  $('#addToInventoryButton').bind('click', function()
  {

      //Post Wine to Recommender
      $.post('/Recommend/addFromRecommendToInventory',
      {
          wineID          :  $('#wineModal').attr('wineID'),
          locationID    :  $('#locationDropDown').val().slice(0,$('#locationDropDown').val().indexOf(' '))

      }, function(data)
      {
          if(data.status == 'INVALID') {
              $('#createErrorMessage').css("display", 'block');
          }else if(data.status == 'VALID'){
              $('#createErrorMessage').css("display", 'none');
              $('.progress_wheel').css("display", 'block');
              location.reload(false);

              $('#inventoryModal').foundation('reveal','close');

          }

      }, 'json');

      return false;

  });
});

  //Make Ajax Request for Candidate Wines
  //This will only fire after a keyboard event has occurred on one of the search boxes AND
  //a certain delay has passed.  Each new keyboard even refreshes the delay.

  $('.autocompleteTextField').keyup(function () {
      typewatch(function () {

        $.post('/Recommend/candidateWines',
        {
              //Create a dictionary that has the current search terms
              wineName   :   $('input[id="autocomplete1"]').val(),
              winery     :   $('input[id="autocomplete2"]').val(),
              vintage    :   $('input[id="autocomplete3"]').val()
          }, function(data)
          {


            if(data.status == 'INVALID') {
                    //alert('IT R BROKE K?');
                    //Clear the candidate list
                    $('#candyWineList').empty();
                }else if(data.status == 'VALID'){

                  //Clear the candidate list
                  $('#candyWineList').empty();

                    //For each candidate, build a div and add an on click listener
                    var cand;
                    for(var i = 0; i < data.candidates.length; i++) {
                        cand = data.candidates[i];

                        function slicer(str) {
                          var streak = 0;
                          for(var i = 0 ; i < str.length; i++)
                          {
                            if(str.charAt(i) != ' ') {
                              streak += 1;
                          }else{
                              streak = 0;
                          }

                          if(streak > 30) {
                              str = str.slice(0,i) + ' ' + str.slice(i);
                              streak = 0;
                              i++;
                          }
                      }
                      return str;
                  }

                  cand.wineName = slicer(cand.wineName);
                  cand.winery = slicer(cand.winery);

                    //Construct a massiv div with all of the candidate wine's info and append it to the end of the #candyWineList
                    $('#candyWineList').append('<div class="row candidate-wine-holder" ' +
                        'wineID="' + cand.wineID + '" ' +
                        'wineName="' + cand.wineName + '" ' +
                        'winery="' + cand.winery + '" ' +
                        'vintage="' + cand.vintage + '" ' +
                        'varietal_blend="' + cand.varietal + '" ' +
                        'wineType="' + cand.wineType + '" ' +
                        'region="' + cand.region + '" ' +
                        'tags="' + cand.tags + '" ' +
                        'description="' + cand.description + '" ' +
                        'averageStarRating="' + cand.averageStarRating + '" ' +
                        'imagePath="' + cand.imagePath + '" ' +
                        'bitter="' + cand.bitter + '" ' +
                        'sweet="' + cand.sweet + '" ' +
                        'sour="' + cand.sour + '" ' +
                        'salty="' + cand.salty + '" ' +
                        'chemical="' + cand.chemical + '" ' +
                        'pungent="' + cand.pungent + '" ' +
                        'oxidized="' + cand.oxidized + '" ' +
                        'microbiological="' + cand.microbiological + '" ' +
                        'floral="' + cand.floral + '" ' +
                        'spicy="' + cand.spicy + '" ' +
                        'fruity="' + cand.fruity + '" ' +
                        'vegetative="' + cand.vegetative + '" ' +
                        'nutty="' + cand.nutty + '" ' +
                        'caramelized="' + cand.caramelized + '" ' +
                        'woody="' + cand.woody + '" ' +
                        'earthy="' + cand.earthy + '" ' +
                        '><div class="large-12 columns candidate-wine">' + cand.vintage + ' ' + cand.winery + '\'s ' + cand.wineName +'</div></div>');
}

$('.candidate-wine-holder').each(function() {
    $(this).click(function() {

                  //Remove it from the candidate list
                  $(this).detach();

                  //Attach it to the seed list
                  $('#seedList').append(this);

                  //Remove the on click listener
                  $(this).off('click');

                  //Change its width from large-12 to large-11 to make room for a delete button
                  if($(this).children().eq(0).hasClass('large-12')) {
                    $(this).children().eq(0).removeClass('large-12');
                }
                $(this).children().eq(0).addClass('large-11');
                
                      //Create a delete button
                      var deleteButton = '<div class="large-1 columns delete-button">' + '&#215;' + '</div>';
                      $(this).append(deleteButton);

                  //Give the delete button a listener that removes the seed on click
                  $(this).children().eq(1).click(function() {
                    $(this).parent().remove();
                });
                  
              });
});


}


}, 'json');

        // executed only 500 ms after the last keyup event.
    }, 500);
});

$('.edit_autocompleteTextField').keyup(function () {
  typewatch(function () {

    $.post('/Recommend/candidateWines',
    {
              //Create a dictionary that has the current search terms
              wineName   :   $('input[id="edit_autocomplete1"]').val(),
              winery     :   $('input[id="edit_autocomplete2"]').val(),
              vintage    :   $('input[id="edit_autocomplete3"]').val()
          }, function(data)
          {


            if(data.status == 'INVALID') {
                  //Clear the candidate list
                  $('#candyWineList').empty();
              }else if(data.status == 'VALID'){

                  //Clear the candidate list
                  $('#edit_candyWineList').empty();

                    //For each candidate, build a div and add an on click listener
                    var cand;
                    for(var i = 0; i < data.candidates.length; i++) {
                        cand = data.candidates[i];

                        function slicer(str) {
                            var streak = 0;
                            for(var i = 0 ; i < str.length; i++)
                            {
                              if(str.charAt(i) != ' ') {
                                streak += 1;
                            }else{
                                streak = 0;
                            }

                            if(streak > 30) {
                                str = str.slice(0,i) + ' ' + str.slice(i);
                                streak = 0;
                                i++;
                            }
                        }
                        return str;
                    }

                    cand.wineName = slicer(cand.wineName);
                    cand.winery = slicer(cand.winery);

                    //Construct a massiv div with all of the candidate wine's info and append it to the end of the #candyWineList
                    $('#edit_candyWineList').append('<div class="row edit_candidate-wine-holder" ' +
                        'wineID="' + cand.wineID + '" ' +
                        'wineName="' + cand.wineName + '" ' +
                        'winery="' + cand.winery + '" ' +
                        'vintage="' + cand.vintage + '" ' +
                        'varietal_blend="' + cand.varietal + '" ' +
                        'wineType="' + cand.wineType + '" ' +
                        'region="' + cand.region + '" ' +
                        'tags="' + cand.tags + '" ' +
                        'description="' + cand.description + '" ' +
                        'averageStarRating="' + cand.averageStarRating + '" ' +
                        'imagePath="' + cand.imagePath + '" ' +
                        'bitter="' + cand.bitter + '" ' +
                        'sweet="' + cand.sweet + '" ' +
                        'sour="' + cand.sour + '" ' +
                        'salty="' + cand.salty + '" ' +
                        'chemical="' + cand.chemical + '" ' +
                        'pungent="' + cand.pungent + '" ' +
                        'oxidized="' + cand.oxidized + '" ' +
                        'microbiological="' + cand.microbiological + '" ' +
                        'floral="' + cand.floral + '" ' +
                        'spicy="' + cand.spicy + '" ' +
                        'fruity="' + cand.fruity + '" ' +
                        'vegetative="' + cand.vegetative + '" ' +
                        'nutty="' + cand.nutty + '" ' +
                        'caramelized="' + cand.caramelized + '" ' +
                        'woody="' + cand.woody + '" ' +
                        'earthy="' + cand.earthy + '" ' +
                        '><div class="large-12 columns candidate-wine">' + cand.vintage + ' ' + cand.winery + '\'s ' + cand.wineName +'</div></div>');
}

$('.edit_candidate-wine-holder').each(function() {
    $(this).click(function() {

                  //Remove it from the candidate list
                  $(this).detach();

                  //Attach it to the seed list
                  $('#edit_seedList').append(this);

                  //Remove the on click listener
                  $(this).off('click');

                  //Change its width from large-12 to large-11 to make room for a delete button
                  if($(this).children().eq(0).hasClass('large-12')) {
                    $(this).children().eq(0).removeClass('large-12');
                }
                $(this).children().eq(0).addClass('large-11');
                
                      //Create a delete button
                      var deleteButton = '<div class="large-1 columns delete-button">' + '&#215;' + '</div>';
                      $(this).append(deleteButton);

                  //Give the delete button a listener that removes the seed on click
                  $(this).children().eq(1).click(function() {
                    $(this).parent().remove();
                });
                  
              });
});
}
}, 'json');

        // executed only 500 ms after the last keyup event.
    }, 500);
});

$('#edit_shelfDropDown').change(function() {

    $.post('/Recommend/getSeeds',
    {
              //Create a dictionary that has the current search terms
              recID   :   $('#edit_shelfDropDown').val(),

          }, function(data)
          {

                //Clear the seed list
                $('#edit_seedList').empty();

                var seed;
                for(var i = 0; i < data.seedList.length; i++) {
                  seed = data.seedList[i];

                  function slicer(str) {
                    var streak = 0;
                    for(var i = 0 ; i < str.length; i++)
                    {
                      if(str.charAt(i) != ' ') {
                        streak += 1;
                    }else{
                        streak = 0;
                    }

                    if(streak > 30) {
                        str = str.slice(0,i) + ' ' + str.slice(i);
                        streak = 0;
                        i++;
                    }
                }
                return str;
            }

            seed.wineName = slicer(seed.wineName);
            seed.winery = slicer(seed.winery);

                //Construct a massiv div with all of the seed wine's info and append it to the end of the #seedList
                $('#edit_seedList').append('<div class="row edit_candidate-wine-holder" ' +
                  'wineID="' + seed.wineID + '" ' +
                  'wineName="' + seed.wineName + '" ' +
                  'winery="' + seed.winery + '" ' +
                  'vintage="' + seed.vintage + '" ' +
                  'varietal_blend="' + seed.varietal + '" ' +
                  'wineType="' + seed.wineType + '" ' +
                  'region="' + seed.region + '" ' +
                  'tags="' + seed.tags + '" ' +
                  'description="' + seed.description + '" ' +
                  'averageStarRating="' + seed.averageStarRating + '" ' +
                  'imagePath="' + seed.imagePath + '" ' +
                  'bitter="' + seed.bitter + '" ' +
                  'sweet="' + seed.sweet + '" ' +
                  'sour="' + seed.sour + '" ' +
                  'salty="' + seed.salty + '" ' +
                  'chemical="' + seed.chemical + '" ' +
                  'pungent="' + seed.pungent + '" ' +
                  'oxidized="' + seed.oxidized + '" ' +
                  'microbiological="' + seed.microbiological + '" ' +
                  'floral="' + seed.floral + '" ' +
                  'spicy="' + seed.spicy + '" ' +
                  'fruity="' + seed.fruity + '" ' +
                  'vegetative="' + seed.vegetative + '" ' +
                  'nutty="' + seed.nutty + '" ' +
                  'caramelized="' + seed.caramelized + '" ' +
                  'woody="' + seed.woody + '" ' +
                  'earthy="' + seed.earthy + '" ' +
                  '><div class="large-11 columns candidate-wine">' + seed.vintage + ' ' + seed.winery + '\'s ' + seed.wineName +'</div><div class="large-1 columns delete-button">' + '&#215;' + '</div></div>');

$('.delete-button').click(function() {
    $(this).parent().remove();
});
}
}, 'json');
});

    // Delete wine
    $(function()
    {
        $('#deleteShelfYes').bind('click', function()
        {          
            $.post('/Recommend/delete',
            {
                email   :  '{{ user.emailAddress }}',
                recID   :   $('#edit_shelfDropDown').val(),

            }, function(data)
            {
                if(data.status == 'VALID') {
                    $('#deleteErrorMessage').css("display", 'none');
                //Reload page
                location.reload(false);
            }else{
                $('#deleteErrorMessage').css("display", 'block');
            }
        }, 'json');

//            $('#deleteShelfModal').trigger('reveal:close');
});
    });

    //data-reveal-id="wineInfoModal"


    function bindWineModalClick() {
      $('[data-reveal-id="wineModal"]').bind('click', function()
      {

          var viewWineModal = $('#wineModal');
          var staticPath = '{{ url_for('static', filename='images/wine/') }}';

          $('#wineModal').attr('wineID', $(this).attr('wine-wineID'));

          //alert($(this).attr('wine-wineName'));
          $('#wine_wineName').text($(this).attr('wine-wineName'));
          $('#wine_winery').text($(this).attr('wine-winery'));
          $('#wine_varietal').text($(this).attr('wine-varietal'));
          $('#wine_vintage').text($(this).attr('wine-vintage'));
          $('#wine_averageStarRating').text($(this).attr('wine-averageStarRating'));
          $('#wine_region').text($(this).attr('wine-region'));
          $('#user_quantity').text($(this).attr('user-quantity'));
          $('#user_tags').text($(this).attr('user-tags'));
          $('#user_description').text($(this).attr('user-description'));
          $('#user_isWishlist').text($(this).attr('user-isWishlist'));
          $('#user_personalStarRating').text($(this).attr('user-personalStarRating'));

          //Image fall-back code
          var imagePath = $(this).attr('user-imagePath');
          if(imagePath == null || imagePath == '' || imagePath == 'None')
              imagePath = $(this).attr('wine-imagePath');
          if(imagePath == null || imagePath == '' || imagePath == 'None')
              imagePath = 'default_wine.jpg';
          $('#user_imagePath').attr('src', staticPath + imagePath);

          $('#wineModal').foundation('reveal', 'open');

          return false;

      });
}

$(function()
{
  bindWineModalClick();
});

var typewatch = (function()
{
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
}  
})();


var rec_con = $('#recommendation-container');
$('#progress_wheel_container').css("display", 'none');
rec_con.css("display", 'block');


var typewatch2 = (function()
{
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    }  
})();

typewatch2(function () {
    //Fix for chrome
    $('#recommendation-container').isotope({ filter: '.recommended-' + $('.channel-button:first').attr('shelf-id') });
}, 500);


var modalwatch = (function()
{
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    }  
})();


