<script>
  import {
    Header,
    HeaderUtilities,
    HeaderAction,
    HeaderGlobalAction,
    HeaderPanelLinks,
    HeaderPanelDivider,
    HeaderPanelLink,
    SideNav,
    SideNavItems,
    SideNavMenu,
    SideNavMenuItem,
    SideNavLink,
    SkipToContent,
    Theme,
  } from "carbon-components-svelte";
  import SettingsAdjust from "carbon-icons-svelte/lib/SettingsAdjust.svelte";

  let isSideNavOpen = false;
  let isOpen2 = false;
  let theme = "g90";
</script>

<Header platformName="arcadian" bind:isSideNavOpen>
  <svelte:fragment slot="skip-to-content">
    <SkipToContent />
  </svelte:fragment>
  <HeaderUtilities>
    <HeaderGlobalAction aria-label="Settings" icon={SettingsAdjust} />
    <HeaderAction bind:isOpen={isOpen2}>
      <HeaderPanelLinks>
        <Theme persist persistKey="__carbon-theme" render="select" />
      </HeaderPanelLinks>
    </HeaderAction>
  </HeaderUtilities>
</Header>
