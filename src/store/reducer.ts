import {ActionType, StateAction} from "./actions";

export type SystemState = {
  sidebarNavVisible: boolean;
};

const initialState: SystemState = {
  sidebarNavVisible: false
}

export const reducer = (state: SystemState = initialState, action: StateAction): SystemState => {
  switch (action.type) {
    case ActionType.SIDEBAR_NAV_SHOW: {
      return {
        ...state,
        sidebarNavVisible: true
      };
    }
    case ActionType.SIDEBAR_NAV_HIDE: {
      return {
        ...state,
        sidebarNavVisible: false
      };
    }
    case ActionType.SIDEBAR_NAV_TOGGLE: {
      return {
        ...state,
        sidebarNavVisible: !state.sidebarNavVisible
      };
    }
    default: {
      return state;
    }
  }
};

export default reducer;
