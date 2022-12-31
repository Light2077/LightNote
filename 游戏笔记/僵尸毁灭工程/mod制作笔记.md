https://docs.qq.com/doc/DYk16WE1aSk1iZmdl

解析script下的txt脚本

```python
def get_re_match(pattern, item, group=1):
    match = re.search(pattern, item)
    if match:
        return match.group(1)
    
def get_key_value(key, item_str):
    value = get_re_match(f'{key} *= *(.*?),', item)
    return value

with open(r'D:\Software\steam\steamapps\common\ProjectZomboid\media\scripts\items.txt') as f:
    text = f.read()
text = re.sub('\n', ' ', text)
text = re.sub('\t', ' ', text)
# 删除所有注释
# re.sub(r'/\*.*?\*/', '', text)
```

匹配所有items

```python
items = re.findall(r'item [a-zA-Z]+ +\{.*?\}', text)
item = items[0]
item
```

获取名字和key value

```python
item_name = get_re_match(r'item (\w+)', item)
weight = get_key_value('Weight', item)
```



## 自己的mod

我想搞一个物品转移速度加快、建造速度加快的mod。

### 转移速度加快

ISInventoryTransferAction.lua

ISDropWorldItemAction.lua

ISDropItemAction.lua

```lua
if character:HasTrait("Dextrous") then
    o.maxTime = o.maxTime * 0.5
end
if character:HasTrait("AllThumbs") then
    o.maxTime = o.maxTime * 4.0
end
```

### 家具搬运拆解加快

ISMoveablesAction.lua

### 建筑速度加快

ISBuildAction.lua

```lua
function ISBuildAction:new(character, item, x, y, z, north, spriteName, time)
	local o = {}
	setmetatable(o, self)
	self.__index = self
	o.character = character;
	o.item = item;
	o.x = x;
	o.y = y;
	o.z = z;
	o.north = north;
	o.spriteName = spriteName;
	o.stopOnWalk = true;
	o.stopOnRun = true;
	o.maxTime = time;
    o.craftingBank = item.craftingBank;
	if character:HasTrait("Handy") then
		-- o.maxTime = time - 50;
        o.maxTime = time * 0.05
    end
--    o.maxTime = 500;
    o.square = getCell():getGridSquare(x,y,z);
    o.doSaw = false;
    o.caloriesModifier = 8;
	return o;
end
```



### 其他

ISDismantleAction.lua 猜测是拆电子产品的动作

ISDestroyStuffAction.lua 物品摧毁动作

ISUnbarricadeAction.lua 受到特质 Handy影响，但是不知道是影响了什么

ISBarricadeAction.lua 同上



## 免费字体特效网

https://www.logosc.cn/text/

## 脚本代码

一键获取文件夹下所有mod信息

```python
data_dir = r'D:\Software\steam\steamapps\workshop\content\108600'
def get_mod_id_by_info(mod_info_text):
    mod_id = re.search(r'id=(.*?)$', mod_info_text, flags=re.M).group(1)
    mod_name = re.search(r'name=(.*?)$', mod_info_text, flags=re.M).group(1)
    return mod_id, mod_name
mod_info_paths = glob.glob(os.path.join(data_dir, '**\mod.info'),recursive=True)

mod_infos = []
for p in mod_info_paths:
    m = re.search(r'\\(\d{7,})\\', p)
    with open(p, encoding='utf8') as f:
        text = f.read()
        
    mod_id, mod_name = get_mod_id_by_info(text)
    workshop_id = m.group(1)
    mod_infos.append([mod_id, workshop_id, mod_name])
mod_infos = pd.DataFrame(mod_infos)
mod_infos.columns = ['mod id', 'workshop id', 'mod name']
```

