BASE_URL = "https://raw.githubusercontent.com/maxtrussell/computercraft-python/"

args = {...}
branch = args[1] or "master"

function getFile(filename)
	-- download file from github
	local resp = http.get(BASE_URL .. branch .. filename)
	if resp == nil then
		print("Download failed for " .. BASE_URL .. branch .. filename)
		return
	end

	-- write file
	local file = fs.open(filename, "w")
	file.write(resp.readAll())
	file.close()
end

getFile("/download_code.py")
shell.run("wget http://localhost:6969/ py")

shell.run("py /download_code.py " .. branch)
