    processor 6502
    include vcs.h
SPX = $80
SPY = $81
Invader = $F300
Rocket  = $F310
Colors  = $F3A0
    ORG $F000
Start
    sei
    cld
    ldx #$FF
    txs
    lda #0
Clear
    sta 0,x
    dex
    bne Clear
    lda #76
    sta SPY
    lda #50
    sta SPX
Frame
    lda #2
    sta VBLANK
    sta VSYNC
    sta WSYNC
    sta WSYNC
    sta WSYNC
    lda #0
    sta VSYNC
    lda #43
    sta TIM64T
    lda Colors
    sta COLUBK
    lda Colors+2
    sta COLUP0
    lda Colors+3
    sta COLUP1
    lda SWCHA
    asl
    bcs NoRight
    inc SPX
NoRight
    asl
    bcs NoLeft
    dec SPX
NoLeft
    asl
    bcs NoDown
    inc SPY
NoDown
    asl
    bcs NoUp
    dec SPY
NoUp
    lda SPX
    cmp #200
    bcc NotWrap
    lda #0
    sta SPX
NotWrap
    cmp #152
    bcc XOk
    lda #151
    sta SPX
XOk
    lda SPX
    ldx #0
    jsr Position
    lda #110
    ldx #1
    jsr Position
    sta WSYNC
    sta HMOVE
Wait
    lda INTIM
    bne Wait
    sta WSYNC
    sta VBLANK
    ldx #0
Line
    txa
    sec
    sbc SPY
    cmp #16
    bcs No0
    lsr
    tay
    lda Invader,y
    bcc Do0
    bcs Do0
No0
    lda #0
Do0
    sta WSYNC
    sta GRP0
    txa
    sec
    sbc #88
    cmp #16
    bcs No1
    lsr
    tay
    lda Rocket,y
    bcc Do1
    bcs Do1
No1
    lda #0
Do1
    sta GRP1
    inx
    cpx #192
    bne Line
    lda #2
    sta VBLANK
    lda #35
    sta TIM64T
Over
    lda INTIM
    bne Over
    jmp Frame
Position
    sta WSYNC
    sec
Div
    sbc #15
    bcs Div
    eor #7
    asl
    asl
    asl
    asl
    sta HMP0,x
    sta RESP0,x
    rts
End
    ORG $FFFC
    .word Start
    .word Start
