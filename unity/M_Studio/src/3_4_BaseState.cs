public abstract class BaseState
{
    // 用于判定是哪个敌人的状态，野猪、蜜蜂、蜗牛
    protected Enemy currentEnemy;

    public abstract void OnEnter(Enemy enemy);
    
    // 撞墙等逻辑判断，在update中执行
    public abstract void LogicUpdate();
    public abstract void PhysicsUpdate();
    public abstract void OnExit();
}