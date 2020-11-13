import {createContext} from "react";
import {Consumer} from "../common/types";

export type OverlayState = {
  sidebarNavVisible: boolean;
};

type OverlayStateContextType = {
  overlayState: OverlayState,
  setOverlayState: Consumer<OverlayState>
}

const OverlayStateContext = createContext<OverlayStateContextType>({
  overlayState: {
    sidebarNavVisible: false
  },
  setOverlayState: () => console.error("OverlayStateContext not initialized."),
});

export default OverlayStateContext;
