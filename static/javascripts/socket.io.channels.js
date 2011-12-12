(function() {
    var prototype = io.Socket.prototype;
    io.Socket = function(host, options) {
        options = options || {};
        return prototype.constructor.call(this, host, options);
    };
    // We need to reassign all members for the above to work.
    for (var name in prototype) {
        io.Socket.prototype[name] = prototype[name];
    }
    // Set up the subscription methods.
    io.Socket.prototype.subscribe = function(channel) {
        this.send(['__subscribe__', channel]);
        return this;
    };
    io.Socket.prototype.unsubscribe = function(channel) {
        this.send(['__unsubscribe__', channel]);
        return this;
    };
})();
