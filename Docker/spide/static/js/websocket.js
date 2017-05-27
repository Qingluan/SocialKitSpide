function web_client(url){
	var ws = new WebSocket(url); //"ws://localhost:8080/socket"
	
	ws.onopen = function() {
	   ws.send("Hello, world");

	};

	this.on_msg = function(callback){
		ws.onmessage = function (evt) {
	    console.log(evt.data);
		    if (callback){
				callback(JSON.parse(evt.data));	
		    }
	   
		};		
	}
	
}

