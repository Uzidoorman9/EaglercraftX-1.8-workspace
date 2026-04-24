package net.minecraft.client.gui;

import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiScreen;

public class GuiAbout extends GuiScreen {

    private GuiScreen parent;

    public GuiAbout(GuiScreen parent) {
        this.parent = parent;
    }

    @Override
    public void initGui() {
        this.buttonList.clear();

        // Back button
        this.buttonList.add(new GuiButton(0, this.width / 2 - 100, this.height - 40, "Back"));
    }

    @Override
    protected void actionPerformed(GuiButton button) {
        if (button.id == 0) {
            this.mc.displayGuiScreen(parent);
        }
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        this.drawDefaultBackground();

        // Title
        this.drawCenteredString(this.fontRendererObj, "About", this.width / 2, 40, 0xFFFFFF);

        // Content (edit this however you want)
        this.drawCenteredString(this.fontRendererObj, "Your Eaglercraft Mod", this.width / 2, 70, 0xAAAAAA);
        this.drawCenteredString(this.fontRendererObj, "Version 1.0", this.width / 2, 85, 0xAAAAAA);
        this.drawCenteredString(this.fontRendererObj, "Made by Cyn", this.width / 2, 100, 0xAAAAAA);

        super.drawScreen(mouseX, mouseY, partialTicks);
    }
}