export enum ActionType {
  SIDEBAR_NAV_SHOW,
  SIDEBAR_NAV_HIDE,
  SIDEBAR_NAV_TOGGLE
}

export type StateAction =
  | { type: ActionType.SIDEBAR_NAV_SHOW }
  | { type: ActionType.SIDEBAR_NAV_HIDE }
  | { type: ActionType.SIDEBAR_NAV_TOGGLE };

export const StateActionFactory = {
  showSidebarNav: () => { return { type: ActionType.SIDEBAR_NAV_SHOW } },
  hideSidebarNav: () => { return { type: ActionType.SIDEBAR_NAV_HIDE } },
  toggleSidebarNav: () => { return { type: ActionType.SIDEBAR_NAV_TOGGLE } },
};
