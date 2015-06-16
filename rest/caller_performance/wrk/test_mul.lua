counter = 0

request = function()
  path = "/call?seq=" .. counter
  counter = counter + 1
  wrk.method = "POST"
  wrk.headers["Content-Type"] = "application/json"
  wrk.body = "{\"procedure\": \"com.example.mul2\", \"args\": [2, 3], \"kwargs\": {\"verbose\": false}}"
  return wrk.format("POST", path)
end

