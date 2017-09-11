-- utils.lua
-- =========
-- Module with general utility functions

local utils = {};
local input_dir = '../game/inputs.txt';
local cheat_dir = '../game/cheats.txt';


local function poll_file(filename)
    local file = io.open(filename, 'r');

    if file ~= nil then
        contents = file:read('*a');
        file:close();
    end

    return contents;
end


local function reset_file(filename)
    for i = 1, 10 do
        local file = io.open(filename, 'w');

        if file ~= nil then
            file:close();
            break;
        else
            os.execute('sleep 1');
        end
    end
end


function utils.split(string, delimiter)
    if delimiter == nil or string == nil then
        return;
    end

    split_string = {};

    for match in string.gmatch(contents, '([^' .. delimiter .. ']+)') do
        table.insert(split_string, match);
    end

    return split_string;
end


-- removes trailing whitespace
function utils.trim_string(input)
    if input == nil then
        return nil;
    end

    return tostring(input):gsub('^%s*(.-)%s*$', '%1');
end


-- checks if there's an input from twitch and returns the input, if any
-- inputs.txt contents in format "([1-9%w+] )*[1-9]%w+" (letters matching a button)
function utils.poll_input()
    contents = utils.trim_string(poll_file(input_dir));
    return utils.split(contents, ' ');
end


-- same as poll_input for cheat file
function utils.poll_cheat()
    return utils.trim_string(poll_file(cheat_dir));
end


-- erases input file contents
function utils.reset_input_file()
    reset_file(input_dir);
end


-- erases cheat file contents
function utils.reset_cheat_file()
    reset_file(cheat_dir);
end


return utils;
