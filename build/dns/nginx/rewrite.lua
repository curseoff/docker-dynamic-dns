local routes = _G.routes

if routes == nil then
    routes = {}
    ngx.log(ngx.ALERT, "[[[Route cache is empty.]]")
end

local container_name = string.sub(ngx.var.http_host, 1, string.find(ngx.var.http_host, "%.")-1)
local route = routes[container_name]
if route == nil then
    local Redis  = require "nginx.redis"
    local client = Redis:new()

    client:set_timeout(1000)
    local ok, err = client:connect("127.0.0.1", 6379)
    if not ok then
        ngx.log(ngx.ERR, "************ Redis connection failure: " .. err)
        return
     end

    route = client:get(container_name)
end

ngx.log(ngx.ALERT, route)

-- fallback to redis for lookups
if route ~= nil then
    ngx.var.upstream = route
    routes[container_name] = route
else
    ngx.log(ngx.ALERT, "=ng=[[[route null]]]")
    ngx.exit(ngx.HTTP_NOT_FOUND)
end