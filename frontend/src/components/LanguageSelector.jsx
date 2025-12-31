import React from 'react';
import { Globe } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const LanguageSelector = () => {
    const { language, setLanguage, t } = useLanguage();

    return (
        <select
            className="lang-selector"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
        >
            <option value="en">{t('languages.en')}</option>
            <option value="te">{t('languages.te')}</option>
            <option value="hi">{t('languages.hi')}</option>
        </select>
    );
};

export default LanguageSelector;
