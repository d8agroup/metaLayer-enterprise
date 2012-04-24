from metalayercore.visualizations.controllers import VisualizationController
from django.utils import simplejson as json

"""
Extensions to MetaLayer Enterprise that are used as part of Providentia.

Utility functions are added here to avoid adding Providentia-specific code to the
dashboard and metalayercore modules.

"""

def render_javascript_based_visualization(config, search_results_collection, search_configuration):
    """
    Replaces the metalayercore.visualizations.googlegeochart.visualization method.
    
    """
    search_results = search_results_collection[0]
    facets = [f['facets'] for f in search_results['facet_groups'] if f['name'] == config['data_dimensions'][0]['value']['value']][0]
    
    location_entries = {}
    
    #print 'content items'
    #print search_results_collection
    
    #print 'facet groups'
    #print search_results['facet_groups']
    
    #print search_results['content_items']

    for item in search_results['content_items']:
        
        if 'action_yahooplacemaker_location_s' not in item:
            continue
            
        for location in item['action_yahooplacemaker_location_s']:
            
            if location == '_none':
                continue
                
            if location not in location_entries:
                location_entries[location] = [item]
            else:
                location_entries[location].append(item)
    
    viz = VisualizationController.LoadVisualization(config['name'])
    
    # background stuff
    background_color, empty_region_color = _background_colors(config)
    
    # parameters for JavaScript stuff
    parameters = {
        'displayMode': [e for e in config['elements']][0]['value'],
        'region': viz._map_map_focus([e for e in config['elements']][1]['value']),
        'background_color': background_color,
        'empty_region_color': empty_region_color,
    }
    
    geodata_statements = ""
    location_details_statements = ""
    
    # map and location details
    for i in range(len(facets)):
        f = facets[i]
        
        geodata_statements += """
        geoData.setValue(%d, 0, %r);
        geoData.setValue(%d, 1, %d);
        geoData.setFormattedValue(%d, 1, '%d');
        geoData.setValue(%d, 2, %d);
        geoData.setFormattedValue(%d, 2, '(Click marker for details)');
        """ % (
            i, str(f['name']),
            i, _MARKER_COLORS['RED'],
            i, f['count'],
            i, _MARKER_COLORS['RED'],
            i,
            )
        
    
    
    js = """
        $.getScript
        (
            'https://www.google.com/jsapi',
            function()
            {
                google.load('visualization', '1', {'packages': ['geochart'], 'callback':drawRegionsMap});
                
                function drawRegionsMap() {
                    geoData = new google.visualization.DataTable();
                    geoData.addRows(%d);
                    geoData.addColumn('string', 'Country');
                    geoData.addColumn('number', 'Mentions');
                    geoData.addColumn('number', 'Details');
                    
                    // start geo data
                    %s
                    // end geo data
                    
                    // start location details
                    location_details = %s
                    // end location details
                    
                    var options = {};
                    options['region'] = %r;
                    options['colorAxis'] = { minValue : 0, maxValue : 1, colors : ['#0000FF','#FF0000', '#00FF00']};
                    options['backgroundColor'] = %r;
                    options['datalessRegionColor'] = %r;
                    options['legend'] = 'none';
                    options['displayMode'] = %r;
                    
                    var geochart = new google.visualization.GeoChart(document.getElementById('v_test'));
                    
                    google.visualization.events.addListener(geochart, 'select', function() {
                        var selected_location = geoData.getValue(geochart.getSelection()[0].row, 0);
                        
                        display_location_dialog(selected_location);
                        
                    });
                    
                    geochart.draw(geoData, options);
                }
            }
        );
    """ % (
            len(facets),
            geodata_statements,
            json.dumps(location_entries),
            parameters['region'],
            parameters['background_color'],
            parameters['empty_region_color'],
            parameters['displayMode'],
        )
        
    return js

def _background_colors(config):
    
    background = [e for e in config['elements'] if e['name'] == 'background'][0]['value']
    if background == 'Dark':
        background_color = '#333333'
        empty_region_color = '#CCCCCC'
    else:
        background_color = '#F8F6F6'
        empty_region_color = '#CCCCCC'
    
    return background_color, empty_region_color

# Contains the position of a given color in the geochart's color axis
_MARKER_COLORS = {
    'RED': 0,
    'GREEN': 2,
    'BLUE': 1,
}

