import React, { createContext, useContext, useMemo } from "react";
import en from "./en.json";
import hi from "./hi.json";
import { useSettingsStore } from "../stores/settingsStore";

type Dict = Record<string, string>;
const dicts: Record<string, Dict> = { en, hi };

type I18n = { t: (k: string) => string; lang: string };
const I18nCtx = createContext<I18n>({ t: (k) => k, lang: "en" });

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const lang = useSettingsStore((s) => s.lang);
  const value = useMemo(() => {
    const d = dicts[lang] || dicts.en;
    return { lang, t: (k: string) => d[k] || dicts.en[k] || k };
  }, [lang]);
  return <I18nCtx.Provider value={value}>{children}</I18nCtx.Provider>;
}

export function useI18n() {
  return useContext(I18nCtx);
}

