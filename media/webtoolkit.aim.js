/**
*
*  AJAX IFRAME METHOD (AIM)
*  http://www.webtoolkit.info/
*
**/
 
AIM = {
 
	frame : function(c) {
 
		var n = 'f' + Math.floor(Math.random() * 99999);
		var d = document.createElement('iframe');
		d.innerHTML = '';
		document.body.appendChild(d).setAttribute('id',n);console.log('frame-exists');
 
		var i = document.getElementById(n);
		if (c && typeof(c.onComplete) == 'function') {
			i.onComplete = c.onComplete;console.log('complete-set');
		}
 
		return n;
	},
 
	form : function(f, name) {
		f.setAttribute('target', name);
	},
 
	submit : function(f, c) {
		AIM.form(f, AIM.frame(c));
		if (c && typeof(c.onStart) == 'function') {
			console.log('go');return c.onStart();
		} else {
			return true;
		}
	},
 
	loaded : function(id) {
		var i = document.getElementById(id);
		if (i.contentDocument) {
			var d = i.contentDocument;
		} else if (i.contentWindow) {
			var d = i.contentWindow.document;
		} else {
			var d = window.frames[id].document;
		}
		if (d.location.href == "about:blank") {
			return;
		}
 
		if (typeof(i.onComplete) == 'function') {
			i.onComplete(d.body.innerHTML);console.log('complete-finish');
		}
	}
 
}