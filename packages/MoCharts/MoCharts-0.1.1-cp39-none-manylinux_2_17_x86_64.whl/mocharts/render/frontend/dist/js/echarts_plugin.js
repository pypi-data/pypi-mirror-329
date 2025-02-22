function support_popup(option, height, width, inner_html) {
  option['toolbox']['feature']['myFeature'] = {
    show: true,
    title: 'Open in new window',
    icon: 'image://https://raw.githubusercontent.com/CnBDM-Su/XAI_demo/master/popup_icon.png',
    onclick: function (){
      var height_ = Math.min(screen.height, Math.round(1.5 * parseInt(height.slice(0,-2))))
      var width_ = Math.min(screen.width, Math.round(1.5 * parseInt(width.slice(0,-2))))
      var left = (screen.width/2)-(width_/2);
      var top = (screen.height/2)-(height_/2);
      var win = window.open('template.html', '_blank',
        `height=${height_}px, width=${width_}px, top=${top}px, left=${left}px`,
      );
      win.document.write(`${inner_html}`);
      win.document.close();
    }
  };
  return option;
};