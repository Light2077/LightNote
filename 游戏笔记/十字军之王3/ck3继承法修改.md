使得玩家能够专属获得长子继承法（参考自mod 2773747483）

主要要有3个步骤：

- 创建一个获取长子继承法的决议
- 创建一个王朝modifier
- 修改继承法文件

### 决议创建

`common\decisions\xxx_mod_decision.txt`

```perl
pbd_single_heir_succession_law_decision = {
	picture = "gfx/interface/illustrations/decisions/decision_dynasty_house.dds"
	major = yes
	desc = pbd_single_heir_succession_law_decision_desc
	ai_check_interval = 0
	
	# 法律不是长子或幼子继承法时显示该决议
	is_shown = {
		NOR = { 
		    has_realm_law = single_heir_succession_law
		    has_realm_law = single_heir_succession_law_youngest
		}
	}
	# 能显示就能点
	is_valid = {
        # custom_tooltip = pbd_single_heir_succession_law_decision_valid_tooltip
		is_adult = yes
	}
	
	effect = {
		custom_tooltip = pbd_single_heir_succession_law_decision_effect_tooltip
		# 触发一个事件用于选择长子或幼子继承制
		trigger_event = pdb_major_decisions.0001
        dynasty = {
		 	add_dynasty_modifier = {
		 		modifier = pbd_single_heir_succession_law_decision_modifier
		    }
	    }
    }
	ai_will_do = {
		base = 0
	}
}
```

### 事件创建

`events/pbd_events.txt`

```perl
pdb_major_decisions.0001 = {
	type = character_event
	title = pdb_major_decisions.0001.t
	desc = pdb_major_decisions.0001.desc
	theme = physical_health
	left_portrait = {
		character = root
		animation = personality_bold
	}
	override_background = { event_background = throne_room }
	
	immediate = {
		play_music_cue = "mx_cue_positive_effect"
		# strengthen_bloodline_decision_effects = yes
	}
    # 前面的代码都无关紧要

    # 长子继承法
	option = {
		name = pdb_major_decisions.0001.option.a
        add_realm_law_skip_effects = single_heir_succession_law
	}

    # 幼子继承法
    option = {
		name = pdb_major_decisions.0001.option.b
        add_realm_law_skip_effects = single_heir_succession_law_youngest
	}

    # 无事发生
    option = {
		name = pdb_major_decisions.0001.option.c
	}
}
```





### 修正创建

modifier 图标的文件：`gfx\interface\icons\modifiers`

modifier 文件：`common\modifiers`

创建`common/modifiers/pdb_modifiers.txt`

```perl
pbd_single_heir_succession_law_decision_modifier = {
	icon = county_modifier_corruption_positive
    dynasty_opinion = 5  # 同一宗族好感
}
```

### 继承法修改

`common\scripted_triggers\00_law_triggers.txt`

```perl
can_keep_single_heir_succession_law_trigger = {
	# The 'can_keep' triggers are dependent on actually having the law. If they aren't, the trigger breakdown for the player breaks and shows incomplete information.
	trigger_if = {
		limit = {
			has_realm_law = single_heir_succession_law
		}
		OR = {
			dynasty = { has_dynasty_modifier = pbd_single_heir_succession_law_decision_modifier }
			can_have_single_heir_succession_law_trigger = yes
			# Byzantine Empire
			historical_succession_access_single_heir_succession_law_trigger = yes
		}
	}
}
can_keep_single_heir_youngest_succession_law_trigger = {
	# The 'can_keep' triggers are dependent on actually having the law. If they aren't, the trigger breakdown for the player breaks and shows incomplete information.
	trigger_if = {
		limit = {
			has_realm_law = single_heir_succession_law_youngest
		}
		OR = {
			dynasty = { has_dynasty_modifier = pbd_single_heir_succession_law_decision_modifier }
			can_have_single_heir_youngest_succession_law_trigger = yes
			historical_succession_access_single_heir_succession_law_youngest_trigger = yes
		}
	}
}
```

### 本地化

```
l_simp_chinese:
 pbd_single_heir_succession_law_decision:0 "继承法改革"
 pbd_single_heir_succession_law_decision_desc:0 "我们的宗族在继承法上有超越时代的理解。"
 pbd_single_heir_succession_law_decision_effect_tooltip:0 "允许使用长嗣继承法或幼嗣继承法。"
 pbd_single_heir_succession_law_decision_modifier:0 "钦定继承"
 pbd_single_heir_succession_law_decision_confirm:0 "改革继承法"
 pdb_major_decisions.0001.t:0 "继承法改革"
 pdb_major_decisions.0001.desc:0 "长久以来，各大领主都采用分割继承法，这无疑会削弱后代的实力，而我们宗族采用更加优越的单一继承法，这将会使我们越来越强大。"
 pdb_major_decisions.0001.option.a:0 "采用长嗣继承法"
 pdb_major_decisions.0001.option.b:0 "采用幼嗣继承法"
 pdb_major_decisions.0001.option.c:0 "容我三思"
```



