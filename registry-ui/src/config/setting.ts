/**
 * 全局配置接口定义
 */
interface SettingConfig {
  /** token传递的header名称 */
  tokenHeaderName: string;
  /** token存储的名称 */
  tokenAccessName: string;
  /** token存储的名称 */
  tokenRefreshName: string;
  /** 获取缓存的token */
  takeToken: () => string | null;
  /** 缓存token */
  cacheToken: (token: string | null, remember?: boolean) => void;
  /** 获取缓存的用户信息 */
  takeUser: () => Record<string, any>;
  /** 缓存用户信息 */
  cacheUser: (user: Record<string, any> | null) => void;
}

const setting: SettingConfig = {
  tokenHeaderName: "Authorization",
  tokenAccessName: "access_token",
  tokenRefreshName: "refresh_token",

  takeToken(): string | null {
    let token = localStorage.getItem(this.tokenAccessName);
    if (!token) {
      token = sessionStorage.getItem(this.tokenAccessName);
    }
    return token;
  },

  cacheToken(token: string | null, remember?: boolean): void {},

  takeUser(): Record<string, any> {
    return {};
  },

  cacheUser(user: Record<string, any> | null): void {},
};

export default setting;
export type { SettingConfig };
