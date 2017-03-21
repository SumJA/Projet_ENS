@PostConstruct
@Override
public void postConstruct() {
    super.postConstruct();

    getResultsTable().setMultiSelect(true);

    HorizontalLayout crudButtons = new HorizontalLayout();
    setDebugId(crudButtons, "crudButtons");
    crudButtons.setMargin(false);
    crudButtons.setSpacing(true);

    newButton = new Button(uiMessageSource.getMessage("crudResults.new"), this, "create");
    newButton.setDescription(uiMessageSource.getToolTip("crudResults.new.toolTip"));
    newButton.setIcon(new ThemeResource("../expressui/icons/16/add.png"));
    newButton.addStyleName("small default");
    crudButtons.addComponent(newButton);

    viewButton = new Button(uiMessageSource.getMessage("crudResults.view"), this, "view");
    viewButton.setDescription(uiMessageSource.getToolTip("crudResults.view.toolTip"));
    viewButton.setIcon(new ThemeResource("../expressui/icons/16/view.png"));
    viewButton.addStyleName("small default");
    crudButtons.addComponent(viewButton);

    editButton = new Button(uiMessageSource.getMessage("crudResults.edit"), this, "edit");
    editButton.setDescription(uiMessageSource.getToolTip("crudResults.edit.toolTip"));
    editButton.setIcon(new ThemeResource("../expressui/icons/16/edit.png"));
    editButton.addStyleName("small default");
    crudButtons.addComponent(editButton);

    deleteButton = new Button(uiMessageSource.getMessage("crudResults.delete"), this, "delete");
    deleteButton.setDescription(uiMessageSource.getToolTip("crudResults.delete.toolTip"));
    deleteButton.setIcon(new ThemeResource("../expressui/icons/16/delete.png"));
    deleteButton.addStyleName("small default");
    crudButtons.addComponent(deleteButton);

    actionContextMenu.addAction("crudResults.view", this, "view");
    actionContextMenu.addAction("crudResults.edit", this, "edit");
    actionContextMenu.addAction("crudResults.delete", this, "delete");

    addSelectionChangedListener(this, "selectionChanged");
    getCrudButtons().addComponent(crudButtons, 0);
    getCrudButtons().setComponentAlignment(crudButtons, Alignment.MIDDLE_LEFT);

    getResultsTable().addListener(new DoubleClickListener());

    addCodePopupButtonIfEnabledForCrudResults();
}