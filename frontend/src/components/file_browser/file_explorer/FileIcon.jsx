import React, { useEffect, useState } from "react";

import { ReactComponent as ClosedArrowIcon } from "./img/arrowSide.svg";
import { ReactComponent as OpenArrowIcon } from "./img/arrowDown.svg";
import { ReactComponent as ClosedFolderIcon } from "./img/closedFolder.svg";
import { ReactComponent as OpenFolderIcon } from "./img/openFolder.svg";
import { ReactComponent as BaseFileIcon } from "./img/file.svg";

function FileIcon({ is_dir, is_collapsed, name, group }) {
  if (is_dir) {
    if (is_collapsed) {
      return (
        <>
          <ClosedArrowIcon className="arrow-icon" stroke={"var(--icon)"} />
          <ClosedFolderIcon className="arrow-icon" fill={"var(--icon)"} />
        </>
      );
    } else {
      return (
        <>
          <OpenArrowIcon className="arrow-icon" stroke={"var(--icon)"} />
          <OpenFolderIcon className="arrow-icon" fill={"var(--icon)"} />
        </>
      );
    }
  } else {
    return (
      <>
        <BaseFileIcon className="arrow-icon" fill={"var(--icon)"} />
      </>
    );
  }
}

export default FileIcon;
