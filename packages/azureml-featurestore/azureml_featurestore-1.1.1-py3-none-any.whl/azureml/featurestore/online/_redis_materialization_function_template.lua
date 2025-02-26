-- ---------------------------------------------------------
-- Copyright (c) Microsoft Corporation. All rights reserved.
-- ---------------------------------------------------------
-- IMPORTANT
-- Any string declared in bracket varName format should have its value replaced by the python script.
-- Expected dataformat should be
-- keys_cols = Contains all the name of each key
-- values_cols = Contains all the name of each value
-- Each row of data should be
-- [key1,key2,...keyN, value1, value2,...valueN, timestamp_value, time_to_live_value]
-- The 2nd to last index of each record should be time stamp value.
-- The last index of each row data should be TTL.
-- timestamp_value and ttl value should be in string format.
local key_cols = {keyColsFormat}
local value_cols = {valueColsFormat}
local key_prefix = {keyPrefixFormat}
local time_stamp_col = {timestampColFormat}
local ttl_exist = {timeToLiveExistFormat}
-- LUA array starts at 1
local key = key_prefix
-- This loop will calculate the redis key
for key_index = 1, #key_cols do
    key = key .. key_cols[key_index] .. ':'
    key = key .. ARGV[key_index]
end

-- This loop should check for all the redis value_cols
local old_timestamp = redis.pcall('hget', key, time_stamp_col)
if (old_timestamp == false) then
    old_timestamp = -1
else
    old_timestamp = tonumber(old_timestamp)
end

local time_stamp_index = #key_cols + #value_cols + 1
-- Timestamp always come right after key and value columns
local new_timestamp = tonumber(ARGV[time_stamp_index])
if (new_timestamp >= old_timestamp) then
    for value_index = 1, #value_cols do
        local value_index_offset_by_keys = value_index + #key_cols
        local value_name = value_cols[value_index]
        local value_to_store = ARGV[value_index_offset_by_keys]
        redis.pcall('hset', key, value_name, value_to_store)
    -- Store the timestamp column
    end
    redis.pcall('hset', key, time_stamp_col, new_timestamp)
    -- Expire the current row of data if ttl exist
    if (ttl_exist) then
        redis.pcall('expire', key, tonumber(ARGV[#ARGV]))
    end
end
