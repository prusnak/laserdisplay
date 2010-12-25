var svgCanvas = null;

$(function(){

    svgCanvas = new SvgCanvas(document.getElementById("svgcanvas"));

    svgCanvas.setMode('fhpath');
    svgCanvas.setStrokeWidth(3);
    svgCanvas.setStrokeColor('#ffffff');
    svgCanvas.setFillColor('none');

    $('#select').click(function(){ svgCanvas.setMode('select'); });
    $('#path').click(function(){ svgCanvas.setMode('fhpath'); });
    $('#line').click(function(){ svgCanvas.setMode('line'); });
    $('#rect').click(function(){ svgCanvas.setMode('rect'); });
    $('#ellipse').click(function(){ svgCanvas.setMode('ellipse'); });

    $('#clear').click(function(){ svgCanvas.clear(); });
    $('#delete').click(function(){ svgCanvas.deleteSelectedElements(); });

    $('#color_white').click(function(){ svgCanvas.setStrokeColor('#ffffff'); });
    $('#color_red').click(function(){ svgCanvas.setStrokeColor('#ff0000'); });
    $('#color_green').click(function(){ svgCanvas.setStrokeColor('#00ff00'); });
    $('#color_blue').click(function(){ svgCanvas.setStrokeColor('#0000ff'); });
    $('#color_cyan').click(function(){ svgCanvas.setStrokeColor('#00ffff'); });
    $('#color_magenta').click(function(){ svgCanvas.setStrokeColor('#ff00ff'); });
    $('#color_yellow').click(function(){ svgCanvas.setStrokeColor('#ffff00'); });

    $('#template1').click(function(){ svgCanvas.insertTemplate(template1); });
    $('#template2').click(function(){ svgCanvas.insertTemplate(template2); });
    $('#template3').click(function(){ svgCanvas.insertTemplate(template3); });
    $('#template4').click(function(){ svgCanvas.insertTemplate(template4); });
    $('#template5').click(function(){ svgCanvas.insertTemplate(template5); });

});
