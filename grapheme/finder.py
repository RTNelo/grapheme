from grapheme import GraphemePropertyGroup as G
from grapheme import get_group


class FSM:
    @classmethod
    def default(cls, n):
        if n is G.OTHER:
            return True, cls.default

        if n is G.CR:
            return True, cls.cr

        if n in [G.LF, G.CONTROL]:
            return True, cls.lf_or_control

        if n is G.ZWJ:
            return False, cls.zwj

        if n in [G.EXTEND, G.SPACING_MARK]:
            return False, cls.default

        if n in [G.E_BASE, G.E_BASE_GAZ]:
            return True, cls.emoji

        if n is G.REGIONAL_INDICATOR:
            return True, cls.ri

        if n is G.L:
            return True, cls.hangul_l

        if n in [G.LV, G.V]:
            return True, cls.hangul_lv_or_v

        if n in [G.LVT, G.T]:
            return True, cls.hangul_lvt_or_t

        if n is G.PREPEND:
            return True, cls.prepend
        # todo: add rules
        return True, cls.default

    @classmethod
    def default_next_state(cls, n, should_break):
        _, next_state = cls.default(n)
        return should_break, next_state

    @classmethod
    def cr(cls, n):
        if n is G.LF:
            return False, cls.lf_or_control
        return cls.default_next_state(n, should_break=True)

    @classmethod
    def lf_or_control(cls, n):
        return cls.default_next_state(n, should_break=True)

    @classmethod
    def prepend(cls, n):
        if n in [G.CONTROL, G.LF]:
            return True, cls.default
        if n is G.CR:
            return True, cls.cr
        return cls.default_next_state(n, should_break=False)

    # Hanguls
    @classmethod
    def hangul_l(cls, n):
        if n in [G.V, G.LV]:
            return False, cls.hangul_lv_or_v
        if n is G.LVT:
            return False, cls.hangul_lvt_or_t
        if n is G.L:
            return False, cls.hangul_l
        return cls.default(n)

    @classmethod
    def hangul_lv_or_v(cls, n):
        if n is G.V:
            return False, cls.hangul_lv_or_v
        if n is G.T:
            return False, cls.hangul_lvt_or_t
        return cls.default(n)

    @classmethod
    def hangul_lvt_or_t(cls, n):
        if n is G.T:
            return False, cls.hangul_lvt_or_t
        return cls.default(n)

    # Emojis
    @classmethod
    def emoji(cls, n):
        if n is G.EXTEND:
            return False, cls.emoji
        if n is G.E_MODIFIER:
            return False, cls.default
        return cls.default(n)

    @classmethod
    def zwj(cls, n):
        if n is G.GLUE_AFTER_ZWJ:
            return False, cls.default
        if n is G.E_BASE_GAZ:
            return False, cls.emoji
        return cls.default(n)

    # Regional indication (flag)
    @classmethod
    def ri(cls, n):
        if n is G.REGIONAL_INDICATOR:
            return False, cls.default
        return cls.default(n)


def graphemes(string):
    buffer = string[0]
    _, state = FSM.default(get_group(buffer))
    print(state )

    for codepoint in string[1:]:
        current_group = get_group(codepoint)
        should_break, state = state(current_group)
        print(should_break, state)
        if should_break:
            yield buffer
            buffer = codepoint
        else:
            buffer += codepoint

    if buffer:
        yield buffer

    raise StopIteration()
