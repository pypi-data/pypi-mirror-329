# django-model-helper

Helpful django abstract models collection.

## 抽象类列表

- WithAddModTimeFields
- WithArgsKwargsFields
- WithConfigFields
- WithCountFields
- WithDeletedStatusFields
- WithDisplayOrderFields
- WithEnabledStatusFields
- WithExpireTimeFields
- WithHitsFields
- WithHotspotFields
- WithInitiatorFields
- WithJsonDataFields
- WithLockStatusFields
- WithOwnerFields
- WithPublishStatusFields
- WithSimpleNRRDStatusFields
- WithSimplePRSFStatusFields
- WithSimpleResultFields
- WithUidFields
- WithUserFields
- WithUserFields
- WithVisibleFields

## 版本记录

### v0.1.0

- 版本首发。

### v0.1.1

- WithExpireTimeFields添加default_expires属性。
- WithUidFields添加uidgen属性，用于生成uid默认值。

### v0.1.5

- 添加WithVisibleFields抽象类。
- 添加WithHotspotFields抽象类。

### v0.1.9

- 添加WithArgsKwargsFields抽象类。
- 修正强制要求`GLOBAL_LOCK_CONFIG`配置项的问题。

### v0.1.12

- 添加`WithSimpleResultFields.result_time`字段。
- 添加`WithEnabledStatusFields`的action机制。
    - 添加`actions.set_enabled_for_selected`和`actions.set_disabled_for_selected`。
    - 添加`admin.WithEnabledStatusFieldsAdmin`.
    - 添加`WithEnabledStatusFields.Meta.permissions`.
    - 添加`WithEnabledStatusFields.enabled_display`.
- 添加`WithDeletedStatusFields`的action机制。
    - 添加`actions.set_deleted_for_selected`和`actions.set_undeleted_for_selected`。
    - 添加`admin.WithDeletedStatusFieldsAdmin`.
    - 添加`WithDeletedStatusFields.Meta.permissions`.
    - 添加`WithDeletedStatusFields.set_undeleted`和`WithDeletedStatusFields.deleted_display`.
- 添加`WithVisibleFields`的action机制。
    - 添加`actions.set_visible_for_selected`和`actions.set_hidden_for_selected`。
    - 添加`admin.WithVisibleFieldsAdmin`.
    - 添加`WithVisibleFields.Meta.permissions`.
    - 添加`WithVisibleFields.visible_display`.
- 添加`WithHotspotFields`的action机制。
    - 添加`actions.set_hotspot_for_selected`和`actions.clear_hotspot_for_selected`。
    - 添加`admin.WithHotspotFieldsAdmin`.
    - 添加`WithHotspotFields.Meta.permissions`.
    - 添加`WithHotspotFields.hotspot_display`.
    - 修改`WithHotspotFields.set_non_hotspot`为`WithHotspotFields.clear_hotspot`。
- **注意：所有相关模型都需要做模型更新。即：`python manage.py migrate`**

### v0.2.0

- 添加`WithHitsFields`抽象模型。
- 添加`WithPublishFields`抽象模型。
- 添加`WithOwnerFields`抽象模型。
- 添加`WithInitiatorFields`抽象模型。
- 添加`WithSimplePRSFStatusFields`抽象模型。
- 修改`WithCountFields`抽象类的增减机制，删除`globallock`依赖，添加`WithCountFields.last_count_changed_time`字段。
- 修改`WithArgsKwargs`抽象模型使用yaml进行序列化。
- 修改`WithEnabledStatusFields`抽象模型增加`auto_enable`的设置，默认为true表示自动启用。

### v0.2.1

- 添加`pydantic`依赖关系。
- 删除`django-redis`依赖关系。

### v0.2.2

- 在`WithXXXAdmin`中添加关联的`actions`。
- 在`WitnOwnerFields`中添加`is_owenr`方法。
- 在`WithInitiatorFields`中添加`is_initiator`方法。
- 引入i18n来处理字段名称（部分）。
