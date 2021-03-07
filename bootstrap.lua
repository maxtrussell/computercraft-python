BASE_URL = "https://raw.githubusercontent.com/maxtrussell/computercraft-python/master"

function getFile(filename)
	-- download file from github
	local resp = http.get(BASE_URL .. filename)
	if resp == nil then
		print("Download failed for " .. BASE_URL .. filename)
		return
	end

	-- write file
	local file = fs.open(filename, "w")
	file.write(resp.readAll())
	file.close()
end

getFile("/download_code.py")
shell.run("wget http://localhost:6969/ py")

args = {...}
branch = args[1] or "master"
shell.run("py /download_code.py " .. branch)
