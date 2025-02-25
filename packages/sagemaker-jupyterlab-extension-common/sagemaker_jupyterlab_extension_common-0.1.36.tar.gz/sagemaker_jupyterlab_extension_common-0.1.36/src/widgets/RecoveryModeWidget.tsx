import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Dialog } from '@jupyterlab/apputils';
import { recoveryModeIcon } from '../components/icons';
import { DialogAlertIcon, DialogBox, StatusBarAlertIcon, StatusBarWidget } from './styles/icons/styles';

// Dialog Logic
const openDialog = async () => {
  const dialog = new Dialog({
    title: (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <recoveryModeIcon.react className={DialogAlertIcon} />
        Runtime is in recovery mode
      </div>
    ),
    body: (
      <div className={DialogBox}>
        <div>Amazon SageMaker Studio is running in recovery mode with limited functionalities</div>
        <br />
        <div>
          Recovery mode is useful to troubleshoot and resolve configuration issues that prevent your regular workspace
          from starting.
        </div>
      </div>
    ),
    buttons: [Dialog.okButton({ label: 'Dismiss' })],
  });

  await dialog.launch();
};

// Widget Definition
class RecoveryModeWidget extends ReactWidget {
  constructor() {
    super();
  }

  render(): JSX.Element {
    return (
      <div className={StatusBarWidget} onClick={() => openDialog()} title="Click to view recovery mode information">
        <recoveryModeIcon.react className={StatusBarAlertIcon} />
        Runtime in Recovery Mode
      </div>
    );
  }
}

export { RecoveryModeWidget };
