var paneLoader = function(data, paneId) {
    el = getElement(paneId);
    el.innerHTML = data.responseText;
}

var failedLoad = function(err) {
    alert("failed to load pane data");
}

var loadSlots = []
var loadURLs = []

LoadStuff = function () {
    var req = doSimpleXMLHttpRequest(loadURLs[0])
    req.addCallbacks(function(data){paneLoader(data,loadSlots[0])}, failedLoad);
};