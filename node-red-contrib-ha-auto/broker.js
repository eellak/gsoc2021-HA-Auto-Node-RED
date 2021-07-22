module.exports = function(RED) {
    function BrokerNode(config) {
        RED.nodes.createNode(this, config);
        const node = this;
        const msg = {
            payload: {
                name: this.name,
                host: config.host,
                port: config.port,
                b_type: config.b_type,
                username: config.username,
                password: config.password,
                db: config.db,
                exchange: config.exchange
            }
        }
        node.send(msg);
    }
    RED.nodes.registerType("broker", BrokerNode);
}