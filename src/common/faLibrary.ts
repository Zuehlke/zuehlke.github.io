import {library} from "@fortawesome/fontawesome-svg-core";
import {fab} from "@fortawesome/free-brands-svg-icons";
import {faBars, faTimes} from "@fortawesome/free-solid-svg-icons";

const initFaLibrary = () => {
  library.add(fab, faBars, faTimes);
};

export default initFaLibrary;
