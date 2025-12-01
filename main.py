from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# Hier speichern wir die HWIDs: { "HWID": TIMESTAMP }
authorized_hwids = {}

# Wie lange soll der Key halten? (24 Stunden in Sekunden)
DURATION = 86400 

def cleanup_old_keys():
    """Löscht abgelaufene HWIDs um Speicher zu sparen"""
    current_time = time.time()
    to_remove = [hwid for hwid, timestamp in authorized_hwids.items() if current_time - timestamp > DURATION]
    for k in to_remove:
        del authorized_hwids[k]

# --- HTML DESIGN FÜR DIE VERIFY SEITE ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Script Verification</title>
    <style>
        body { background-color: #1a1a1a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background-color: #2b2b2b; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); text-align: center; }
        h2 { color: #00ff88; }
        .btn { background-color: #008cff; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 5px; cursor: pointer; transition: 0.3s; }
        .btn:hover { background-color: #006bbd; }
        .info { margin-top: 15px; font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Antibot Verification</h2>
        <p>Bitte bestätige, dass du ein Mensch bist.</p>
        <br>
        <form method="POST" action="/verify_action">
            <input type="hidden" name="hwid" value="{{ hwid }}">
            <button type="submit" class="btn">Ich bin kein Roboter (VERIFY)</button>
        </form>
        <p class="info">Deine HWID: {{ hwid }}</p>
    </div>
</body>
</html>
"""

HTML_SUCCESS = """
<!DOCTYPE html>
<html>
<body style="background-color: #1a1a1a; color: #00ff88; text-align: center; padding-top: 100px; font-family: sans-serif;">
    <h1>Erfolgreich verifiziert!</h1>
    <p style="color: white;">Du hast nun für 24 Stunden Zugriff.</p>
    <p>Geh zurück in das Spiel und drücke "Check Key".</p>
</body>
</html>
"""

@app.route('/')
def home():
    return "Server is online."

# Das ist die Seite, auf die der User nach Linkvertise kommt
@app.route('/auth')
def auth_page():
    hwid = request.args.get('hwid')
    if not hwid:
        return "Fehler: Keine HWID gefunden. Bitte starte das Script neu."
    return render_template_string(HTML_PAGE, hwid=hwid)

# Das passiert, wenn man den Knopf drückt
@app.route('/verify_action', methods=['POST'])
def verify_action():
    hwid = request.form.get('hwid')
    if hwid:
        cleanup_old_keys() # Alte Keys löschen
        authorized_hwids[hwid] = time.time() # HWID whitelisten
        return render_template_string(HTML_SUCCESS)
    return "Fehler."

# Das Roblox Script fragt hier an
@app.route('/check_status')
def check_status():
    hwid = request.args.get('hwid')
    cleanup_old_keys()
    
    if hwid in authorized_hwids:
        # Prüfen ob 24h vorbei sind
        if time.time() - authorized_hwids[hwid] < DURATION:
            return "true"
    
    return "false"

# Hier kommt dein eigentliches Script rein (Raw Text)
@app.route('/get_script')
def get_script():
    hwid = request.args.get('hwid')
    if hwid in authorized_hwids:
         # HIER DEIN SCRIPT EINFÜGEN:
        return """
--[[
    Professional Smart-Cache Loader
    - Checks for local files (No redownload if exists)
    - Uses getcustomasset for local images
    - High-Performance 'Exponential' animations
    - Secure Execution
]]

local TweenService = game:GetService("TweenService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

-- // CONFIGURATION \\ --
local FILE_NAME_LOGO = "Loader_Cache_Logo_v1.png"
local FILE_NAME_SCRIPT = "Loader_Cache_Script_v1.lua"

local URL_LOGO = "https://files.catbox.moe/7f1i0u.png"
local URL_SCRIPT = "https://pastebin.com/raw/SWAWuH0N"

-- // FILESYSTEM FUNCTIONS \\ --
-- Checks if your executor supports necessary functions
local function isSupported()
    return (writefile and readfile and isfile and getcustomasset)
end

local function getAsset(path, url, updateStatusFunc)
    if isfile(path) then
        -- Optimization: File exists, skip download
        if updateStatusFunc then updateStatusFunc("Retrieving from Cache: " .. path) end
        task.wait(0.1) -- Tiny artificial delay just so user sees the check happened
        return getcustomasset(path)
    else
        -- File missing: Download it
        if updateStatusFunc then updateStatusFunc("Downloading Asset...") end
        local content = game:HttpGet(url)
        writefile(path, content)
        return getcustomasset(path)
    end
end

local function getScriptContent(path, url, updateStatusFunc)
    if isfile(path) then
        -- Optimization: Read local file
        if updateStatusFunc then updateStatusFunc("Reading Local Script...") end
        task.wait(0.2)
        return readfile(path)
    else
        -- File missing: Download it
        if updateStatusFunc then updateStatusFunc("Downloading Payload...") end
        local content = game:HttpGet(url)
        writefile(path, content)
        return content
    end
end

-- // UI CONSTRUCTION \\ --
local LocalPlayer = Players.LocalPlayer
local GUI_PARENT = (game:GetService("CoreGui") or LocalPlayer.PlayerGui)

-- Cleanup old instances
if GUI_PARENT:FindFirstChild("SmartLoader") then
    GUI_PARENT.SmartLoader:Destroy()
end

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "SmartLoader"
ScreenGui.IgnoreGuiInset = true
ScreenGui.ResetOnSpawn = false
ScreenGui.Parent = GUI_PARENT

-- Main Container
local MainFrame = Instance.new("Frame")
MainFrame.Name = "MainFrame"
MainFrame.Size = UDim2.new(0, 0, 0, 0) -- Start invisible
MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
MainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
MainFrame.BackgroundColor3 = Color3.fromRGB(18, 18, 18) -- "Perfect Dark"
MainFrame.BorderSizePixel = 0
MainFrame.ClipsDescendants = true
MainFrame.Parent = ScreenGui

local UICorner = Instance.new("UICorner")
UICorner.CornerRadius = UDim.new(0, 12)
UICorner.Parent = MainFrame

local Glow = Instance.new("ImageLabel")
Glow.Name = "Glow"
Glow.BackgroundTransparency = 1
Glow.Position = UDim2.new(0, -15, 0, -15)
Glow.Size = UDim2.new(1, 30, 1, 30)
Glow.Image = "rbxassetid://5028857472"
Glow.ImageColor3 = Color3.fromRGB(0, 0, 0)
Glow.ImageTransparency = 0.6
Glow.ScaleType = Enum.ScaleType.Slice
Glow.SliceCenter = Rect.new(24, 24, 276, 276)
Glow.Parent = MainFrame

-- Logo
local Logo = Instance.new("ImageLabel")
Logo.Name = "Logo"
Logo.Size = UDim2.new(0, 90, 0, 90)
Logo.Position = UDim2.new(0.5, 0, 0.3, 0)
Logo.AnchorPoint = Vector2.new(0.5, 0.5)
Logo.BackgroundTransparency = 1
Logo.ImageTransparency = 1 -- Start invisible for fade in
Logo.Parent = MainFrame

-- Status Text
local StatusText = Instance.new("TextLabel")
StatusText.Name = "Status"
StatusText.Size = UDim2.new(1, 0, 0, 20)
StatusText.Position = UDim2.new(0.5, 0, 0.65, 0)
StatusText.AnchorPoint = Vector2.new(0.5, 0.5)
StatusText.BackgroundTransparency = 1
StatusText.Font = Enum.Font.GothamBold
StatusText.Text = "SYSTEM INITIALIZED"
StatusText.TextColor3 = Color3.fromRGB(150, 150, 150)
StatusText.TextSize = 12
StatusText.TextTransparency = 1
StatusText.Parent = MainFrame

-- Progress Bar Container
local BarBg = Instance.new("Frame")
BarBg.Name = "BarBg"
BarBg.Size = UDim2.new(0.7, 0, 0, 4)
BarBg.Position = UDim2.new(0.5, 0, 0.8, 0)
BarBg.AnchorPoint = Vector2.new(0.5, 0.5)
BarBg.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
BarBg.BorderSizePixel = 0
BarBg.BackgroundTransparency = 1
BarBg.Parent = MainFrame

local BarCorner = Instance.new("UICorner")
BarCorner.CornerRadius = UDim.new(1, 0)
BarCorner.Parent = BarBg

local BarFill = Instance.new("Frame")
BarFill.Name = "BarFill"
BarFill.Size = UDim2.new(0, 0, 1, 0)
BarFill.BackgroundColor3 = Color3.fromRGB(60, 140, 255) -- Professional Blue
BarFill.BorderSizePixel = 0
BarFill.Parent = BarBg

local FillCorner = Instance.new("UICorner")
FillCorner.CornerRadius = UDim.new(1, 0)
FillCorner.Parent = BarFill

-- // ANIMATION HANDLER \\ --
local function setStatus(text, progress)
    StatusText.Text = string.upper(text)
    
    -- Smooth Progress Tween
    TweenService:Create(BarFill, TweenInfo.new(0.4, Enum.EasingStyle.Exponential, Enum.EasingDirection.Out), {Size = UDim2.new(progress, 0, 1, 0)}):Play()
    
    -- Tiny text pop effect
    local txtTween = TweenService:Create(StatusText, TweenInfo.new(0.2), {TextTransparency = 0.2})
    txtTween:Play()
end

-- // EXECUTION LOGIC \\ --
task.spawn(function()
    
    if not isSupported() then
        warn("Your executor does not support file saving. Using temporary mode.")
    end

    -- 1. Open Animation (Snappy expand)
    local openTween = TweenService:Create(MainFrame, TweenInfo.new(0.5, Enum.EasingStyle.Exponential, Enum.EasingDirection.Out), {Size = UDim2.new(0, 320, 0, 220)})
    openTween:Play()
    task.wait(0.3)
    
    -- Fade in elements
    TweenService:Create(Logo, TweenInfo.new(0.5), {ImageTransparency = 0}):Play()
    TweenService:Create(StatusText, TweenInfo.new(0.5), {TextTransparency = 0}):Play()
    TweenService:Create(BarBg, TweenInfo.new(0.5), {BackgroundTransparency = 0}):Play()
    
    -- 2. Logo Check
    setStatus("Checking Local Assets...", 0.1)
    
    local successLogo, logoAsset = pcall(function()
        return getAsset(FILE_NAME_LOGO, URL_LOGO, function(txt) setStatus(txt, 0.25) end)
    end)
    
    if successLogo and logoAsset then
        Logo.Image = logoAsset
    else
        Logo.Image = URL_LOGO -- Fallback
    end
    
    task.wait(0.3)

    -- 3. Script Check
    setStatus("Verifying Script Integrity...", 0.5)
    
    local scriptContent = ""
    local successScript, result = pcall(function()
        return getScriptContent(FILE_NAME_SCRIPT, URL_SCRIPT, function(txt) setStatus(txt, 0.65) end)
    end)
    
    if successScript then
        scriptContent = result
    else
        setStatus("Cache Failed - Downloading...", 0.7)
        scriptContent = game:HttpGet(URL_SCRIPT)
    end
    
    task.wait(0.2)
    
    -- 4. Execution
    setStatus("Injecting Payload...", 0.9)
    task.wait(0.3)
    
    local loadSuccess, loadErr = pcall(function()
        loadstring(scriptContent)()
    end)
    
    if loadSuccess then
        -- 5. Success Animation
        BarFill.BackgroundColor3 = Color3.fromRGB(100, 255, 120) -- Bright Green
        StatusText.TextColor3 = Color3.fromRGB(100, 255, 120)
        setStatus("Injection Successful", 1)
        
        -- Pulse Effect
        local pulse = TweenService:Create(MainFrame, TweenInfo.new(0.3), {BackgroundColor3 = Color3.fromRGB(25, 30, 25)})
        pulse:Play()
        
        task.wait(1.2)
        
        -- 6. Close Animation (Smooth Shrink)
        local closeTween = TweenService:Create(MainFrame, TweenInfo.new(0.4, Enum.EasingStyle.Exponential, Enum.EasingDirection.In), {Size = UDim2.new(0, 0, 0, 0)})
        closeTween:Play()
        closeTween.Completed:Wait()
        ScreenGui:Destroy()
    else
        -- Error State
        BarFill.BackgroundColor3 = Color3.fromRGB(255, 80, 80)
        StatusText.TextColor3 = Color3.fromRGB(255, 80, 80)
        StatusText.Text = "FATAL ERROR"
        warn("Loader Error:", loadErr)
        task.wait(3)
        ScreenGui:Destroy()
    end
end)
        """
    return "print('Zugriff verweigert!')"

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080)
