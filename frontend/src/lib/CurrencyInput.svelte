<script lang="ts">
  import { TextInput } from "carbon-components-svelte";
  const DEFAULT_LOCALE = "en-US";
  const DEFAULT_CURRENCY = "USD";
  const DEFAULT_NAME = "total";
  const DEFAULT_VALUE = 0;
  const DEFAULT_FRACTION_DIGITS = 2;

  const DEFAULT_CLASS_WRAPPER = "currencyInput";
  const DEFAULT_CLASS_UNFORMATTED = "currencyInput__unformatted";
  const DEFAULT_CLASS_FORMATTED = "currencyInput__formatted";
  const DEFAULT_CLASS_FORMATTED_POSITIVE = "currencyInput__formatted--positive";
  const DEFAULT_CLASS_FORMATTED_NEGATIVE = "currencyInput__formatted--negative";
  const DEFAULT_CLASS_FORMATTED_ZERO = "currencyInput__formatted--zero";

  interface InputClasses {
    wrapper?: string;
    unformatted?: string;
    formatted?: string;
    formattedPositive?: string;
    formattedNegative?: string;
    formattedZero?: string;
  }

  export let value: number = DEFAULT_VALUE;
  export let locale: string = DEFAULT_LOCALE;
  export let currency: string = DEFAULT_CURRENCY;
  export let name: string = DEFAULT_NAME;
  export let required: boolean = false;
  export let disabled: boolean = false;
  export let placeholder: number | null = DEFAULT_VALUE;
  export let isNegativeAllowed: boolean = true;
  export let helperText: string = "";
  export let fractionDigits: number = DEFAULT_FRACTION_DIGITS;
  export let inputClasses: InputClasses | null = null;
  export let light: boolean = false;
  export let size: "sm" | "xl";
  export let labelText: string = "";

  // Formats value as: e.g. $1,523.00 | -$1,523.00
  const formatCurrency = (
    value: number,
    maximumFractionDigits?: number,
    minimumFractionDigits?: number
  ) => {
    return new Intl.NumberFormat(locale, {
      currency: currency,
      style: "currency",
      maximumFractionDigits: maximumFractionDigits || 0,
      minimumFractionDigits: minimumFractionDigits || 0,
    }).format(value);
  };

  // Checks if the key pressed is allowed
  const handleKeyDown = (event: KeyboardEvent) => {
    const isDeletion = event.key === "Backspace" || event.key === "Delete";
    const isModifier = event.metaKey || event.altKey || event.ctrlKey;
    const isArrowKey = event.key === "ArrowLeft" || event.key === "ArrowRight";
    const isTab = event.key === "Tab";
    const isInvalidCharacter = !/^\d|,|\.|-$/g.test(event.key); // Keys that are not a digit, comma, period or minus sign

    if (
      !isDeletion &&
      !isModifier &&
      !isArrowKey &&
      isInvalidCharacter &&
      !isTab
    )
      event.preventDefault();
  };

  let inputTarget: HTMLInputElement;
  const currencyDecimal = new Intl.NumberFormat(locale).format(1.1).charAt(1); // '.' or ','
  const isDecimalComma = currencyDecimal === ",";
  const currencySymbol = formatCurrency(0, 0)
    .replace("0", "") // e.g. '$0' > '$'
    .replace(/\u00A0/, ""); // e.g '0 €' > '€'

  // Updates `value` by stripping away the currency formatting
  const setUnformattedValue = (event?: KeyboardEvent) => {
    if (event) {
      // Don't format if the user is typing a `currencyDecimal` point
      if (event.key === currencyDecimal) return;

      // Pressing `.` when the decimal point is `,` gets replaced with `,`
      if (isDecimalComma && event.key === ".")
        formattedValue = formattedValue.replace(
          /\.([^.]*)$/,
          currencyDecimal + "$1"
        ); // Only replace the last occurence

      // Pressing `,` when the decimal point is `.` gets replaced with `.`
      if (!isDecimalComma && event.key === ",")
        formattedValue = formattedValue.replace(
          /\,([^,]*)$/,
          currencyDecimal + "$1"
        ); // Only replace the last occurence

      // Don't format if `formattedValue` is ['$', '-$', "-"]
      const ignoreSymbols = [currencySymbol, `-${currencySymbol}`, "-"];
      const strippedUnformattedValue = formattedValue.replace(" ", "");
      if (ignoreSymbols.includes(strippedUnformattedValue)) return;

      // Set the starting caret positions
      inputTarget = event.target as HTMLInputElement;

      // Reverse the value when minus is pressed
      if (isNegativeAllowed && event.key === "-") value = value * -1;
    }

    // Remove all characters that arent: numbers, commas, periods (or minus signs if `isNegativeAllowed`)
    let unformattedValue = isNegativeAllowed
      ? formattedValue.replace(/[^0-9,.-]/g, "")
      : formattedValue.replace(/[^0-9,.]/g, "");

    // Finally set the value
    if (Number.isNaN(parseFloat(unformattedValue))) {
      value = 0;
    } else {
      // The order of the following operations is *critical*
      unformattedValue = unformattedValue.replace(
        isDecimalComma ? /\./g : /\,/g,
        ""
      ); // Remove all group symbols
      if (isDecimalComma) unformattedValue = unformattedValue.replace(",", "."); // If the decimal point is a comma, replace it with a period

      // If the zero-key has been pressed
      // and if the current `value` is the same as the `value` before the key-press
      // formatting may need to be done (Issue #30)
      const previousValue = value;
      value = parseFloat(unformattedValue);

      if (event && previousValue === value) {
        // Do the formatting if the number of digits after the decimal point exceeds `fractionDigits`
        if (
          unformattedValue.includes(".") &&
          unformattedValue.split(".")[1].length > fractionDigits
        ) {
          setFormattedValue();
        }
      }
    }
  };

  const setFormattedValue = () => {
    // Previous caret position
    const startCaretPosition = inputTarget?.selectionStart || 0;
    const previousFormattedValueLength = formattedValue.length;

    // Apply formatting to input
    formattedValue = isZero ? "" : formatCurrency(value, fractionDigits, 0);

    // Update `value` after formatting
    setUnformattedValue();

    // New caret position
    const endCaretPosition =
      startCaretPosition + formattedValue.length - previousFormattedValueLength;

    // HACK:
    // Delay setting the new caret position until the input has been formatted
    setTimeout(() => {
      inputTarget?.setSelectionRange(endCaretPosition, endCaretPosition);
    }, 0.1);
  };

  let formattedValue = "";
  let formattedPlaceholder =
    placeholder !== null
      ? formatCurrency(placeholder, fractionDigits, fractionDigits)
      : "";
  $: isZero = value === 0;
  $: isNegative = value < 0;
  $: value, setFormattedValue();
</script>

<div class={inputClasses?.wrapper ?? DEFAULT_CLASS_WRAPPER}>
  <input
    class={inputClasses?.unformatted ?? DEFAULT_CLASS_UNFORMATTED}
    type="hidden"
    {name}
    {disabled}
    bind:value
  />
  <TextInput
    {labelText}
    name={`formatted-${name}`}
    autocomplete="off"
    {light}
    {helperText}
    {disabled}
    {size}
    required={required && !isZero}
    placeholder={formattedPlaceholder}
    bind:value={formattedValue}
    on:keydown={handleKeyDown}
    on:keyup={setUnformattedValue}
    on:blur={setFormattedValue}
  />
</div>

<style>
</style>
